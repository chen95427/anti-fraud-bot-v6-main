"""Claude API 佇列：把「接收使用者請求」跟「真正呼叫 Claude API」拆成兩層。

- submit_job() 立刻回 job_id，HTTP 請求不用卡著等 Claude。
- 固定數量的 worker thread 依序從佇列撈工作呼叫 Claude；worker 數＝同時最多幾個請求真的在跟 Claude 對話。
- 送出前經過限流器：同時檢查「過去 60 秒請求次數」與「過去 60 秒 input token 總量」，兩者都在安全值內才放行
  （對話愈長，每次重送的歷史愈多，實測先被擋的通常是 ITPM，不是 RPM）。
- 每個工作有逾時上限（從送出起算）；排隊太久或搶不到限流額度，一律回報逾時，不讓請求無限期卡住。
- 鎖只保護純記憶體操作；網路呼叫、I/O、finish 回呼一律在鎖外執行。
"""
import math
import secrets
import threading
import time
from collections import deque

QUEUED, RUNNING, FINISHING, DONE, ERROR, TIMEOUT = 'queued', 'running', 'finishing', 'done', 'error', 'timeout'
_ACTIVE = (QUEUED, RUNNING, FINISHING)

WINDOW_SEC = 60
RESULT_TTL_SEC = 600        # 結束的工作保留 10 分鐘供前端查結果，之後清掉
BUSY_MESSAGE = '系統忙碌，請稍後再試'


class _Job:
    __slots__ = ('id', 'payload', 'status', 'submitted_at', 'deadline', 'started_at',
                 'finished_at', 'result', 'error', 'tokens')

    def __init__(self, job_id, payload, timeout, tokens):
        now = time.time()
        self.id = job_id
        self.payload = payload
        self.status = QUEUED
        self.submitted_at = now
        self.deadline = now + timeout
        self.started_at = None
        self.finished_at = None
        self.result = None
        self.error = None
        self.tokens = tokens


class ClaudeQueue:
    def __init__(self, work_fn, estimate_tokens_fn, num_workers=6, max_requests_per_minute=45,
                 max_input_tokens_per_minute=45000, job_timeout=60,
                 finish_fn=None, actual_tokens_fn=None):
        """work_fn(payload) -> result：真正呼叫 Claude API（在 worker thread、鎖外執行）。
        estimate_tokens_fn(payload) -> int：估算這次呼叫的 input tokens，限流器用。
        finish_fn(payload, result) -> 最終結果（選用）：Claude 回來後的後處理；工作若已逾時就不會執行，
          避免使用者已被告知「忙碌」後，背景又偷偷改動狀態。
        actual_tokens_fn(result) -> int|None（選用）：回來後用實際用量校正限流視窗中的估計值。"""
        self.work_fn = work_fn
        self.estimate_tokens_fn = estimate_tokens_fn
        self.finish_fn = finish_fn
        self.actual_tokens_fn = actual_tokens_fn
        self.num_workers = max(1, int(num_workers))
        self.max_rpm = max(1, int(max_requests_per_minute))
        self.max_itpm = max(1, int(max_input_tokens_per_minute))
        self.job_timeout = job_timeout

        self._lock = threading.Lock()
        self._cond = threading.Condition(self._lock)
        self._jobs = {}                 # job_id -> _Job
        self._queue = deque()           # 排隊中的 job_id（FIFO）
        self._window = deque()          # 限流視窗：[時間, tokens]（list 以便回來後校正 tokens）
        self._running = 0
        self._avg_job_sec = 5.0         # 單筆工作平均耗時（EMA），估計等待秒數用

        for i in range(self.num_workers):
            threading.Thread(target=self._worker_loop, name=f'claude-worker-{i}', daemon=True).start()

    # ---------- 對外介面 ----------
    def submit_job(self, payload):
        try:
            tokens = max(0, int(self.estimate_tokens_fn(payload)))
        except Exception:
            tokens = 0
        job = _Job(secrets.token_urlsafe(16), payload, self.job_timeout, tokens)
        with self._cond:
            self._purge_locked(time.time())
            self._jobs[job.id] = job
            self._queue.append(job.id)
            self._cond.notify()
        return job.id

    def get_status(self, job_id):
        with self._lock:
            job = self._jobs.get(job_id)
            if job is None:
                return {'status': 'unknown'}
            now = time.time()
            self._expire_locked(job, now)
            out = {'status': job.status, 'jobId': job.id}
            if job.status == QUEUED:
                pos = self._queue.index(job.id) + 1
                out.update({'position': pos, 'queueLength': len(self._queue),
                            'etaSeconds': self._eta_locked(pos)})
            elif job.status in (RUNNING, FINISHING):
                out['status'] = RUNNING
            elif job.status == DONE:
                out['result'] = job.result
            elif job.status == ERROR:
                out['error'] = job.error
            elif job.status == TIMEOUT:
                out['error'] = BUSY_MESSAGE
            return out

    def get_queue_stats(self):
        with self._lock:
            now = time.time()
            self._prune_window_locked(now)
            return {'queued': len(self._queue), 'running': self._running,
                    'workers': self.num_workers,
                    'requestsLastMinute': len(self._window), 'maxRequestsPerMinute': self.max_rpm,
                    'inputTokensLastMinute': sum(e[1] for e in self._window),
                    'maxInputTokensPerMinute': self.max_itpm,
                    'avgJobSeconds': round(self._avg_job_sec, 1), 'jobTimeout': self.job_timeout}

    # ---------- worker ----------
    def _worker_loop(self):
        while True:
            with self._cond:
                while not self._queue:
                    self._cond.wait()
                job = self._jobs.get(self._queue.popleft())
                if job is None or job.status != QUEUED:
                    continue
                if time.time() >= job.deadline:
                    self._finish_locked(job, TIMEOUT)
                    continue
                job.status = RUNNING
                job.started_at = time.time()
                self._running += 1
            try:
                self._run(job)
            finally:
                with self._lock:
                    self._running -= 1

    def _run(self, job):
        entry = self._acquire(job)
        if entry is None:
            return                       # 搶不到限流額度直到逾時（已標記 TIMEOUT）
        try:
            result = self.work_fn(job.payload)      # 網路呼叫：鎖外
        except Exception as e:
            print(f'[Queue] 工作失敗 {job.id}: {e}', flush=True)
            with self._lock:
                self._finish_locked(job, ERROR, error='系統暫時無法回應，請稍後再試')
            return
        if self.actual_tokens_fn is not None:
            try:
                actual = self.actual_tokens_fn(result)
                if actual is not None:
                    with self._lock:
                        entry[1] = int(actual)
            except Exception:
                pass
        with self._lock:
            if job.status != RUNNING or time.time() >= job.deadline:
                self._finish_locked(job, TIMEOUT)   # 已逾時：結果丟掉，不跑 finish
                return
            job.status = FINISHING                   # 之後就不會再被判逾時
        if self.finish_fn is not None:
            try:
                result = self.finish_fn(job.payload, result)   # 後處理（可能寫 DB）：鎖外
            except Exception as e:
                print(f'[Queue] 後處理失敗 {job.id}: {e}', flush=True)
                with self._lock:
                    self._finish_locked(job, ERROR, error='系統暫時無法回應，請稍後再試')
                return
        with self._lock:
            self._finish_locked(job, DONE, result=result)

    def _acquire(self, job):
        """等到 RPM 與 ITPM 都有額度才放行；回傳限流視窗中的那筆紀錄，逾時回 None。"""
        while True:
            with self._lock:
                now = time.time()
                if job.status != RUNNING or now >= job.deadline:
                    self._finish_locked(job, TIMEOUT)
                    return None
                self._prune_window_locked(now)
                used = sum(e[1] for e in self._window)
                # 視窗是空的就一定放行（單筆超過上限也不會永遠卡死）
                if not self._window or (len(self._window) < self.max_rpm
                                        and used + job.tokens <= self.max_itpm):
                    entry = [now, job.tokens]
                    self._window.append(entry)
                    return entry
                # 最舊一筆滑出視窗的時間，就是最早可能有額度的時間
                wait = self._window[0][0] + WINDOW_SEC - now
                wait = min(max(wait, 0.05), 1.0, job.deadline - now)
            time.sleep(max(wait, 0.05))   # 等待在鎖外

    # ---------- 以下都需持有鎖、只做記憶體操作 ----------
    def _finish_locked(self, job, status, result=None, error=None):
        if job.status in (DONE, ERROR, TIMEOUT):
            return
        now = time.time()
        if job.status == QUEUED:
            try:
                self._queue.remove(job.id)
            except ValueError:
                pass
        if job.started_at is not None and status == DONE:
            self._avg_job_sec = self._avg_job_sec * 0.8 + (now - job.started_at) * 0.2
        job.status = status
        job.result = result
        job.error = error
        job.finished_at = now
        job.payload = None               # 釋放記憶體（對話歷史等）

    def _expire_locked(self, job, now):
        if job.status in (QUEUED, RUNNING) and now >= job.deadline:
            self._finish_locked(job, TIMEOUT)

    def _eta_locked(self, position):
        # 前面的人 + 自己，平均分給所有 worker；再加上目前處理中那一輪
        rounds = math.ceil(position / self.num_workers)
        return int(math.ceil(rounds * self._avg_job_sec))

    def _prune_window_locked(self, now):
        while self._window and now - self._window[0][0] >= WINDOW_SEC:
            self._window.popleft()

    def _purge_locked(self, now):
        stale = [jid for jid, j in self._jobs.items()
                 if j.status not in _ACTIVE and now - (j.finished_at or now) > RESULT_TTL_SEC]
        for jid in stale:
            del self._jobs[jid]
