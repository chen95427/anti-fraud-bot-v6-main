"""部署前準備：把手冊網站複製到 public/handbook/，讓 Flask 一起 serve。"""

import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

# 可能的手冊路徑（依目前資料夾結構優先排序）
CANDIDATES = [
    PROJECT_ROOT / '員警阻詐教育訓練' / '員警阻詐手冊網站_V2',
    PROJECT_ROOT / '員警阻詐手冊網站_V2',
    PROJECT_ROOT / '員警阻詐手冊網站',
]

src = next((p for p in CANDIDATES if p.exists()), None)
dst = BASE_DIR / 'public' / 'handbook'

if not src:
    print('[WARN] 找不到手冊資料夾，跳過複製')
else:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    print(f'[OK] 已複製手冊：{src} → {dst}')

print('[DONE]')
