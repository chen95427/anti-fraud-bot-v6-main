# 165 AI 反詐訓練網站｜互動式教育訓練平台建置指令

> **給 AI 開發工具（Claude Code / Cursor / Windsurf）的完整建置規格**
> 作者：田心喬醫師　版本：v1.0　2026-04-07

---

## 一、專案定位與目標

### 1.1 用途
員警阻詐溝通技巧的進階教育訓練平台，以「165 AI 反詐被害人心理介入專線」的完整腳本（v2.0）為教材內容，讓員警能在執勤前、演講中、演講後反覆練習。

### 1.2 核心使用場景
| 場景 | 使用方式 |
|------|----------|
| 演講前預習 | 員警自行瀏覽燈號系統、腳本框架 |
| 演講當天 | 投影輔助、示範節點流程 |
| 演講後複習 | 情境測驗、話術快查 |
| 執勤現場 | 手機快查燈號判斷 + 關鍵話術 |

### 1.3 設計風格（與既有網站一致）
- **主色**：深藍 `#1A3C6E`
- **輔色**：中藍 `#2B579A`
- **強調色**：金黃 `#F5C518`
- **警告紅**：`#DC3545`
- **成功綠**：`#28a745`
- **背景**：`#f4f6fb`
- **字體**：微軟正黑體 / Noto Sans TC（Google Fonts 引入）
- **風格**：專業、清晰、政府公務適用、手機友善

---

## 二、整體檔案架構

```
165-training/
├── index.html              ← 訓練首頁（總覽、快速入口）
├── system.html             ← 系統框架（三問定位 + 燈號系統）
├── matrix.html             ← 15組腳本矩陣選擇介面（燈號 × 類型）
├── script-red-chen.html    ← 🔴嗔｜假檢警腳本（8節點完整練習）
├── script-red-tan.html     ← 🔴貪｜投資詐騙腳本
├── script-red-chi.html     ← 🔴癡｜感情詐騙腳本
├── script-red-ao.html      ← 🔴傲｜自我優越型腳本
├── script-red-yi.html      ← 🔴疑｜主動懷疑型腳本
├── script-yellow-chen.html ← 🟡嗔（黃燈版）
├── script-yellow-tan.html  ← 🟡貪（黃燈版）
├── script-yellow-chi.html  ← 🟡癡（黃燈版）
├── script-yellow-ao.html   ← 🟡傲（黃燈版）
├── script-yellow-yi.html   ← 🟡疑（黃燈版）
├── script-green-chen.html  ← 🟢嗔（綠燈版）
├── script-green-tan.html   ← 🟢貪（綠燈版）
├── script-green-chi.html   ← 🟢癡（綠燈版）
├── script-green-ao.html    ← 🟢傲（綠燈版）
├── script-green-yi.html    ← 🟢疑（綠燈版）
├── quiz.html               ← 情境測驗（30題，涵蓋15腳本）
├── quickref.html           ← 快速查詢卡（執勤現場用）
├── style.css               ← 共用樣式
└── data/
    └── scripts.js          ← 所有腳本話術資料（JSON格式）
```

> **優先建置順序**：
> 1. `style.css` → `index.html` → `system.html` → `matrix.html`
> 2. `script-red-chen.html`（作為模板，其他14頁複製此模板）
> 3. `data/scripts.js`（填入所有話術）
> 4. `quiz.html` → `quickref.html`

---

## 三、共用樣式規格（style.css）

```css
/* ===== 基礎重設 ===== */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { font-size: 16px; scroll-behavior: smooth; }
body {
  font-family: 'Noto Sans TC', 'Microsoft JhengHei', sans-serif;
  background: #f4f6fb;
  color: #222;
  line-height: 1.6;
}

/* ===== 色彩變數 ===== */
:root {
  --primary: #1A3C6E;
  --secondary: #2B579A;
  --accent: #F5C518;
  --danger: #DC3545;
  --success: #28a745;
  --bg: #f4f6fb;
  --card: #ffffff;
  --text: #222;
  --muted: #666;
  --border: #dde3ee;

  /* 燈號色 */
  --red: #DC3545;
  --red-light: #fff5f5;
  --yellow: #E6A817;
  --yellow-light: #fffcf0;
  --yellow-passive: #9B59B6;   /* 被動型黃燈用紫色區分 */
  --yellow-passive-light: #f9f0ff;
  --green: #28a745;
  --green-light: #f0fff4;
}

/* ===== 導覽列 ===== */
.topbar {
  background: var(--primary);
  padding: 12px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 8px rgba(0,0,0,0.25);
}
.topbar-title {
  color: white;
  font-size: 15px;
  font-weight: bold;
  text-decoration: none;
  white-space: nowrap;
}
.topbar-nav {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
  justify-content: flex-end;
}
.topbar-nav a {
  color: rgba(255,255,255,0.8);
  text-decoration: none;
  padding: 6px 10px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: bold;
  transition: background 0.2s;
}
.topbar-nav a:hover,
.topbar-nav a.active {
  background: rgba(255,255,255,0.2);
  color: white;
}

/* ===== 主容器 ===== */
.container { max-width: 960px; margin: 0 auto; padding: 24px 16px; }

/* ===== 卡片 ===== */
.card {
  background: var(--card);
  border-radius: 12px;
  border: 1px solid var(--border);
  padding: 20px 24px;
  margin-bottom: 16px;
}
.card-title {
  font-size: 17px;
  font-weight: bold;
  color: var(--primary);
  margin-bottom: 8px;
}

/* ===== 燈號標籤 ===== */
.badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: bold;
  margin-right: 4px;
}
.badge-red    { background: var(--red-light); color: var(--red); border: 1px solid #f5c6cb; }
.badge-yellow { background: var(--yellow-light); color: #856404; border: 1px solid #ffc107; }
.badge-passive{ background: var(--yellow-passive-light); color: var(--yellow-passive); border: 1px solid #ce93d8; }
.badge-green  { background: var(--green-light); color: #155724; border: 1px solid #c3e6cb; }

/* ===== 話術區塊 ===== */
.script-box {
  background: #f8fbff;
  border-left: 4px solid var(--secondary);
  border-radius: 0 8px 8px 0;
  padding: 14px 16px;
  margin: 10px 0;
  font-size: 15px;
  line-height: 1.7;
  color: #1a1a2e;
}
.script-box.version-label {
  font-size: 12px;
  color: var(--muted);
  margin-bottom: 4px;
  font-weight: bold;
}
.purpose-tag {
  background: #e8f0fe;
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 12px;
  color: var(--secondary);
  display: inline-block;
  margin-top: 6px;
}
.timing-tag {
  background: #fef9e7;
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 12px;
  color: #856404;
  display: inline-block;
  margin-top: 4px;
  margin-left: 6px;
}

/* ===== 節點步驟條 ===== */
.node-steps {
  display: flex;
  gap: 0;
  overflow-x: auto;
  margin: 16px 0;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: var(--card);
}
.node-step {
  flex: 1;
  min-width: 70px;
  text-align: center;
  padding: 10px 6px;
  font-size: 12px;
  font-weight: bold;
  color: var(--muted);
  cursor: pointer;
  border-right: 1px solid var(--border);
  transition: background 0.2s, color 0.2s;
  user-select: none;
}
.node-step:last-child { border-right: none; }
.node-step:hover { background: #eef3ff; color: var(--primary); }
.node-step.active {
  background: var(--primary);
  color: white;
}
.node-step .node-num { font-size: 10px; opacity: 0.7; }

/* ===== 版本選擇器 ===== */
.version-tabs {
  display: flex;
  gap: 6px;
  margin: 12px 0 6px;
  flex-wrap: wrap;
}
.version-tab {
  padding: 5px 12px;
  border-radius: 20px;
  border: 1px solid var(--border);
  background: white;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;
  color: var(--muted);
}
.version-tab:hover { border-color: var(--secondary); color: var(--secondary); }
.version-tab.active { background: var(--secondary); color: white; border-color: var(--secondary); }

/* ===== 情境對話框 ===== */
.dialogue-box {
  background: #f0f4ff;
  border-radius: 12px;
  padding: 16px 20px;
  margin: 12px 0;
}
.dialogue-box .speaker {
  font-size: 12px;
  font-weight: bold;
  color: var(--muted);
  margin-bottom: 4px;
}
.dialogue-box .content {
  font-size: 14px;
  line-height: 1.7;
}
.dialogue-box.citizen { background: #fff8e1; }
.dialogue-box.officer { background: #e8f5e9; }
.dialogue-box.arrow   { text-align: center; color: var(--muted); padding: 4px; font-size: 18px; }

/* ===== 測驗元件 ===== */
.quiz-option {
  display: block;
  width: 100%;
  text-align: left;
  padding: 12px 16px;
  margin: 6px 0;
  border: 1px solid var(--border);
  border-radius: 8px;
  background: white;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}
.quiz-option:hover { border-color: var(--secondary); background: #f0f4ff; }
.quiz-option.correct { background: var(--green-light); border-color: var(--success); color: #155724; }
.quiz-option.wrong   { background: var(--red-light);   border-color: var(--danger);  color: var(--danger); }
.quiz-option.disabled { pointer-events: none; }

/* ===== 矩陣格子 ===== */
.matrix-grid {
  display: grid;
  grid-template-columns: 80px repeat(5, 1fr);
  gap: 6px;
  margin: 16px 0;
}
.matrix-header {
  background: var(--primary);
  color: white;
  border-radius: 6px;
  text-align: center;
  padding: 8px 4px;
  font-size: 12px;
  font-weight: bold;
}
.matrix-cell {
  background: white;
  border: 1px solid var(--border);
  border-radius: 8px;
  text-align: center;
  padding: 10px 4px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  color: var(--text);
}
.matrix-cell:hover { box-shadow: 0 2px 8px rgba(26,60,110,0.15); transform: translateY(-1px); }
.matrix-cell .light-icon { font-size: 18px; }
.matrix-cell.red-cell    { border-top: 3px solid var(--red); }
.matrix-cell.yellow-cell { border-top: 3px solid var(--yellow); }
.matrix-cell.green-cell  { border-top: 3px solid var(--green); }

/* ===== 按鈕 ===== */
.btn {
  display: inline-block;
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  text-decoration: none;
  border: none;
  transition: all 0.2s;
}
.btn-primary { background: var(--primary); color: white; }
.btn-primary:hover { background: var(--secondary); }
.btn-outline { background: white; color: var(--primary); border: 2px solid var(--primary); }
.btn-outline:hover { background: var(--primary); color: white; }
.btn-sm { padding: 6px 14px; font-size: 12px; }

/* ===== 快速查詢卡 ===== */
.quickref-card {
  border-radius: 10px;
  padding: 14px 16px;
  margin-bottom: 10px;
  border-left: 5px solid;
}
.quickref-card.red    { background: var(--red-light);    border-color: var(--red); }
.quickref-card.yellow { background: var(--yellow-light); border-color: var(--yellow); }
.quickref-card.green  { background: var(--green-light);  border-color: var(--green); }

/* ===== 響應式 ===== */
@media (max-width: 600px) {
  .topbar { padding: 10px 12px; }
  .topbar-nav a { font-size: 11px; padding: 5px 7px; }
  .container { padding: 16px 12px; }
  .matrix-grid { grid-template-columns: 56px repeat(5, 1fr); font-size: 11px; }
  .node-step { font-size: 11px; min-width: 54px; }
}
```

---

## 四、各頁面規格

### 4.1 首頁（index.html）

**頁面結構：**
```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>165 反詐訓練平台</title>
  <link rel="stylesheet" href="style.css">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&display=swap" rel="stylesheet">
</head>
<body>
  <!-- 導覽列（所有頁面共用，active class 換成當前頁） -->
  <div class="topbar">
    <a class="topbar-title" href="index.html">🛡 165 反詐訓練平台</a>
    <nav class="topbar-nav">
      <a href="index.html" class="active">首頁</a>
      <a href="system.html">系統框架</a>
      <a href="matrix.html">腳本矩陣</a>
      <a href="quiz.html">情境測驗</a>
      <a href="quickref.html">快速查詢</a>
    </nav>
  </div>

  <div class="container">
    <!-- Hero 區塊 -->
    <div class="card" style="background: linear-gradient(135deg, #1A3C6E, #2B579A); color: white; text-align: center; padding: 40px 24px;">
      <div style="font-size: 48px; margin-bottom: 12px;">🛡</div>
      <h1 style="font-size: 24px; margin-bottom: 8px;">165 反詐被害人心理介入</h1>
      <p style="font-size: 15px; opacity: 0.85;">員警進階溝通技巧訓練平台 v2.0</p>
      <p style="font-size: 13px; opacity: 0.7; margin-top: 4px;">新光醫院精神科 田心喬醫師 設計</p>
    </div>

    <!-- 快速入口（4格） -->
    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin: 16px 0;">
      <a href="system.html" class="card" style="text-decoration:none; text-align:center;">
        <div style="font-size:32px; margin-bottom:8px;">🧭</div>
        <div class="card-title">系統框架</div>
        <p style="font-size:13px; color:#666;">三問定位 × 燈號系統<br>看穩聽問守五步驟</p>
      </a>
      <a href="matrix.html" class="card" style="text-decoration:none; text-align:center;">
        <div style="font-size:32px; margin-bottom:8px;">🔢</div>
        <div class="card-title">15組腳本</div>
        <p style="font-size:13px; color:#666;">燈號 × 類型矩陣<br>選擇情境開始練習</p>
      </a>
      <a href="quiz.html" class="card" style="text-decoration:none; text-align:center;">
        <div style="font-size:32px; margin-bottom:8px;">📝</div>
        <div class="card-title">情境測驗</div>
        <p style="font-size:13px; color:#666;">30題情境選擇題<br>測試訓練成效</p>
      </a>
      <a href="quickref.html" class="card" style="text-decoration:none; text-align:center;">
        <div style="font-size:32px; margin-bottom:8px;">⚡</div>
        <div class="card-title">快速查詢</div>
        <p style="font-size:13px; color:#666;">執勤現場速查<br>燈號 × 關鍵話術</p>
      </a>
    </div>

    <!-- 核心框架簡介（看穩聽問守） -->
    <div class="card">
      <div class="card-title">核心框架：擴大版「看穩聽問守」</div>
      <!-- 五步驟橫向卡片，每格含 emoji + 步驟名 + 心理目的 -->
      <!-- 看：多維度評估 / 穩：穩定化 / 聽：深層傾聽 / 問：SCID式引導 / 守：全面守護 -->
    </div>

    <!-- 注意事項卡片 -->
    <div class="card" style="border-left: 4px solid var(--accent);">
      <div class="card-title">⚠ 訓練使用原則</div>
      <ul style="font-size:14px; color:#555; padding-left:20px; line-height:1.8;">
        <li>所有話術以台灣繁體中文呈現，符合在地語言習慣</li>
        <li>永遠不直接說「你被騙了」</li>
        <li>語氣溫柔、非命令式、尊重個案自主性</li>
        <li>先同理，再給資訊</li>
      </ul>
    </div>
  </div>
</body>
</html>
```

---

### 4.2 系統框架頁（system.html）

**區塊順序：**
1. 頁首 Hero：「系統框架：從三問定位到燈號判斷」
2. **三問定位系統**（互動式——點選不同回答會 highlight 對應路徑）
   - 第一問：行為狀態（還在通話中→緊急止損，否→第二問）
   - 第二問：情緒狀態（4個選項→燈號分類）
   - 第三問：詐騙類型初篩（5個選項→類型分類）
3. **燈號系統說明**（4種燈號卡片，每張含核心特徵 + 觸發詞範例）
   - 🔴 紅燈｜🟡 黃燈｜🟡ₚ 被動型黃燈（紫色區分）｜🟢 綠燈
4. **五類型定義**（嗔貪癡傲疑，含心理驅動 + 自殺風險標示）
5. **複合型處理規則**

**三問定位互動邏輯（JavaScript）：**
```javascript
// 點選第一問的「是」→ 顯示「立即進入緊急止損（節點2C）」的高亮提示
// 點選「否」→ 顯示第二問選項
// 點選第二問任一燈號→ 顯示第三問並在燈號卡片上 highlight
// 點選第三問任一類型→ 生成「建議前往：[燈號]×[類型] 腳本」的按鈕連結
```

---

### 4.3 腳本矩陣選擇頁（matrix.html）

**頁面核心：** 一個 4（燈號）× 5（類型）的矩陣，每格都是可點擊的連結。

```
矩陣結構：
         嗔（假檢警） 貪（投資） 癡（感情） 傲（優越） 疑（懷疑）
🔴 紅燈    [連結]      [連結]    [連結]    [連結]    [連結]
🟡 黃燈    [連結]      [連結]    [連結]    [連結]    [連結]
🟡ₚ被動    [連結]      [連結]    [連結]    [連結]    [連結]
🟢 綠燈    [連結]      [連結]    [連結]    [連結]    [連結]
```

每格顯示：
- 燈號 emoji
- 類型名稱
- 自殺風險（高/中/低，用顏色標示）
- 「開始練習」文字

頁面另含：
- 說明卡片：如何使用矩陣（先做三問定位 → 確認燈號 × 類型 → 進入對應腳本）
- 複合型說明：「有多個類型？以情緒強度最高者優先」

---

### 4.4 腳本練習頁模板（以 script-red-chen.html 為例）

這是所有 15 個腳本頁的**通用模板**。其他 14 個腳本頁複製此模板，只需更換：
- `SCRIPT_KEY`（讀取 data/scripts.js 中對應的資料）
- 頁面標題
- 燈號顏色（red/yellow/green）

**頁面結構：**

```html
<!-- 1. 頁首資訊 -->
<div class="card" style="border-top: 4px solid var(--red);">
  <div style="display:flex; align-items:center; gap:12px;">
    <span style="font-size:36px;">🔴</span>
    <div>
      <h1 style="font-size:20px; color:var(--primary);">紅燈 × 嗔｜假檢警詐騙</h1>
      <div>
        <span class="badge badge-red">恐懼型</span>
        <span class="badge" style="background:#fff3cd; color:#856404;">自殺風險：中</span>
        <span class="badge" style="background:#e8f5e9; color:#155724;">8個節點</span>
      </div>
      <p style="font-size:13px; color:#666; margin-top:6px;">核心心理動力：恐懼、司法威脅 ｜ 主要創傷情緒：對體制不信任、羞愧</p>
    </div>
  </div>
</div>

<!-- 2. 節點導航條（點擊切換） -->
<div class="node-steps" id="nodeNav">
  <div class="node-step active" onclick="showNode(1)">
    <div class="node-num">節點1</div>情境判斷
  </div>
  <div class="node-step" onclick="showNode(2)">
    <div class="node-num">節點2</div>依附/止損
  </div>
  <div class="node-step" onclick="showNode(3)">
    <div class="node-num">節點3</div>穩定化
  </div>
  <div class="node-step" onclick="showNode(4)">
    <div class="node-num">節點4</div>偵測保密
  </div>
  <div class="node-step" onclick="showNode(5)">
    <div class="node-num">節點5</div>引導發現
  </div>
  <div class="node-step" onclick="showNode(6)">
    <div class="node-num">節點6</div>不配合應對
  </div>
  <div class="node-step" onclick="showNode(7)">
    <div class="node-num">節點7</div>守
  </div>
  <div class="node-step" onclick="showNode(8)">
    <div class="node-num">節點8</div>風險篩檢
  </div>
</div>

<!-- 3. 節點內容區（JS 控制顯示/隱藏） -->
<div id="node-content">
  <!-- 每個節點的內容，預設只顯示節點1 -->
</div>

<!-- 4. 每個節點的通用格式 -->
<!--
節點標題卡（含目的說明）
↓
版本選擇器（版本1~版本5，或子分類）
↓
版本內容：
  話術框（.script-box）
  心理目的 tag
  使用時機 tag
↓
完整對話示範（可折疊）
↓
下一步導引（→ 節點N的說明）
-->
```

**節點切換 JavaScript：**
```javascript
function showNode(n) {
  // 更新 nodeNav 中的 active class
  document.querySelectorAll('.node-step').forEach((el, i) => {
    el.classList.toggle('active', i + 1 === n);
  });
  // 更新 node-content
  renderNode(n);
  // 捲動到頂部
  window.scrollTo({top: document.getElementById('nodeNav').offsetTop - 60, behavior: 'smooth'});
}

function renderNode(n) {
  const data = SCRIPTS['red-chen'].nodes[n];
  // 根據 data 渲染內容，包含版本選擇器和話術框
}
```

**版本切換 JavaScript：**
```javascript
function showVersion(nodeId, versionNum) {
  // 更新 .version-tab 的 active class
  // 顯示對應版本的 .script-box
}
```

---

### 4.5 腳本資料檔（data/scripts.js）

**資料結構設計（JSON）：**
```javascript
const SCRIPTS = {
  "red-chen": {
    label: "🔴 嗔｜假檢警",
    light: "red",
    type: "chen",
    suicideRisk: "medium",
    psychDrive: "恐懼、司法威脅",
    trauma: "對體制不信任、羞愧",
    nodes: {
      1: {
        title: "情境判斷問句",
        purpose: "確認個案目前的行為狀態，決定後續策略方向",
        versions: [
          {
            label: "最柔和",
            sublabel: "個案極度緊張、拒絕溝通",
            script: "沒關係，我不會催您。我只是想先了解一下——您現在跟對方還有在聯絡嗎？還是在等他的消息？",
            purpose: "先解除對方對AI介入的抗拒，以好奇而非審訊語氣開場",
            timing: "個案一開始就說「你不要管我」「我很急」"
          },
          {
            label: "溫柔關心",
            sublabel: "個案緊張但願意說話",
            script: "我想先了解您現在的狀況，這樣我才能更好地幫您——您現在跟對方還在通話中嗎？還是他在等您做什麼事情？",
            purpose: "把「問問題」框架為「為了幫您」，降低防衛",
            timing: "個案情緒激動但有回應"
          },
          {
            label: "標準版",
            sublabel: "多數情況適用",
            script: "請問您現在跟對方還在通話中，還是他在等您回撥？還是在等您去操作什麼？",
            purpose: "清楚定位行為狀態，三選項涵蓋主要情境",
            timing: "個案情緒中等，願意回答"
          },
          {
            label: "稍微直接",
            sublabel: "個案說情況很急",
            script: "好，我了解時間很急。我先問您一件事：您現在跟對方還在線上嗎？還是他在等您去做什麼？",
            purpose: "先承認緊迫感，再引導回答，避免個案覺得被忽略",
            timing: "個案強調「很急」「來不及了」"
          },
          {
            label: "最果斷",
            sublabel: "確認正在操作中",
            script: "我需要先知道一件事——您現在手上是不是正在做什麼操作？轉帳、ATM、還是網路銀行？",
            purpose: "直接鎖定行為紅燈，不繞彎子",
            timing: "個案說「我在弄」「我在操作」「正在做」"
          }
        ],
        demo: {
          situation: "個案打字很急，說「我很緊張不知道怎麼辦他說三點前要匯」",
          dialogue: [
            { speaker: "AI選擇版本4（個案強調很急）", type: "officer",
              text: "好，我了解時間很急。我先問您一件事：您現在跟對方還在線上嗎？還是他在等您去做什麼？" },
            { speaker: "個案回答", type: "citizen",
              text: "他在等我去ATM他說要我轉到安全帳戶" },
            { speaker: "AI判斷", type: "arrow",
              text: "→ 正在操作情境 → 進入節點2C（緊急止損）" }
          ]
        },
        nextNode: "2A（還在通話中）/ 2B（等回撥）/ 2C（正在操作）"
      },
      2: {
        title: "依附程度判斷 / 緊急止損",
        // ... 節點2A, 2B, 2C 三個子分支
        subNodes: {
          "2A": { title: "依附程度判斷（還在通話中）", /* ... */ },
          "2B": { title: "對方在等回撥（最佳介入時機）", /* ... */ },
          "2C": { title: "緊急止損（正在操作中）", /* ... */ }
        }
      },
      // 節點 3~8 結構相同
    }
  },

  "red-tan": { /* 🔴貪｜投資詐騙 */ },
  "red-chi": { /* 🔴癡｜感情詐騙 */ },
  "red-ao":  { /* 🔴傲｜自我優越型 */ },
  "red-yi":  { /* 🔴疑｜主動懷疑型 */ },
  "yellow-chen": { /* ... */ },
  // ... 其餘10組
};
```

> **⚠ 重要提示給開發者**：
> `data/scripts.js` 的完整話術內容請參照「165AI_v2_全腳本_修正版.docx」原始文件逐一填入。
> 該文件共 19,000 行，包含 15 組腳本 × 8 節點 × 5 版本話術 + 完整對話示範。
> 建議採用「先建框架、再批次填內容」的策略。

---

### 4.6 情境測驗頁（quiz.html）

**規格：**
- 共 30 題，每組腳本各 2 題
- 每題格式：情境描述 → 4 個選項 → 點選後即時顯示對錯 + 解釋
- 結尾：顯示分數 + 各燈號/類型表現分析
- 需要正確答案資料結構（含解釋）

**題目格式範例：**
```javascript
const QUIZ = [
  {
    id: 1,
    category: "red-chen",
    situation: "個案說：「我很緊張，他說帳戶涉及洗錢，三點前要把錢轉到安全帳戶，我不知道怎麼辦」",
    question: "此時個案的燈號判斷為何？最優先的介入方向是？",
    options: [
      { text: "🟡 黃燈，先傾聽個案的感受", correct: false,
        explain: "個案有明顯時間壓力與恐懼，且正在操作中，應判斷為紅燈" },
      { text: "🔴 紅燈，立即進入節點2C緊急止損", correct: true,
        explain: "正確。個案正在操作ATM，是行為紅燈，必須立即啟動緊急止損腳本（節點2C）" },
      { text: "🔴 紅燈，先問依附程度（節點2A）", correct: false,
        explain: "節點2A用於「還在通話中」的情況，此處個案正在操作，應走節點2C" },
      { text: "🟢 綠燈，個案已知道問題所在", correct: false,
        explain: "個案並未懷疑詐騙，而是相信並正在執行，應為紅燈" }
    ]
  },
  // ... 其餘29題
];
```

---

### 4.7 快速查詢卡（quickref.html）

**用途**：執勤現場 30 秒內找到對應話術，手機螢幕友善。

**頁面結構：**
1. 搜尋列（輸入關鍵字即時過濾）
2. 燈號分頁標籤（🔴 / 🟡 / 🟢 切換）
3. 每個燈號下，展示各類型的關鍵節點話術卡片
4. 每張卡片：類型名稱 + 節點 + 1~2 句最重要的話術版本

**快查卡格式：**
```html
<div class="quickref-card red">
  <div style="font-weight:bold; margin-bottom:6px;">🔴 嗔｜假檢警 - 節點2C 緊急止損</div>
  <div style="font-size:14px; line-height:1.7;">
    「我需要請您現在先不要操作。我跟您說一件真正的檢察官不會做的事——」
  </div>
  <a href="script-red-chen.html#node2c" style="font-size:12px; color:var(--secondary);">→ 查看完整5個版本</a>
</div>
```

---

## 五、關鍵功能列表（JavaScript）

### 5.1 三問定位引導器（system.html）
```javascript
// 狀態機
let state = { q1: null, q2: null, q3: null };

function answerQ1(ans) {
  state.q1 = ans;
  if (ans === 'yes') {
    showResult('emergency', '立即進入節點2C（緊急止損）');
  } else {
    showQ2();
  }
}

function answerQ2(light) {
  state.q2 = light;
  highlightLight(light);
  showQ3();
}

function answerQ3(type) {
  state.q3 = type;
  const scriptKey = `${state.q2}-${type}`;
  showResult('navigate', `建議前往：${SCRIPTS[scriptKey].label}`, scriptKey);
}
```

### 5.2 節點切換
```javascript
let currentNode = 1;
let currentVersion = 1;

function showNode(n) {
  currentNode = n;
  currentVersion = 1;
  document.querySelectorAll('.node-step').forEach((el, i) => {
    el.classList.toggle('active', i + 1 === n);
  });
  renderNodeContent(n);
}

function showVersion(v) {
  currentVersion = v;
  document.querySelectorAll('.version-tab').forEach((el, i) => {
    el.classList.toggle('active', i + 1 === v);
  });
  document.querySelectorAll('.version-content').forEach((el, i) => {
    el.style.display = i + 1 === v ? 'block' : 'none';
  });
}
```

### 5.3 測驗邏輯
```javascript
let quizState = {
  current: 0,
  score: 0,
  answers: [],
  categoryScore: {} // { 'red-chen': {correct: 1, total: 2}, ... }
};

function selectOption(optionIndex) {
  const q = QUIZ[quizState.current];
  const opt = q.options[optionIndex];
  // 禁用所有選項
  // 標示正確/錯誤
  // 顯示解釋
  // 記錄到 quizState
  // 顯示下一題按鈕
}

function showResults() {
  // 計算總分、各類別分析
  // 顯示建議加強的腳本連結
}
```

### 5.4 快速查詢過濾
```javascript
function filterQuickRef(keyword) {
  const cards = document.querySelectorAll('.quickref-card');
  cards.forEach(card => {
    card.style.display = card.textContent.includes(keyword) ? 'block' : 'none';
  });
}
```

---

## 六、燈號顏色對應（CSS 變數備查）

| 燈號 | 主色 | 淺色背景 | 說明 |
|------|------|----------|------|
| 🔴 紅燈 | `#DC3545` | `#fff5f5` | 情緒激動、緊急 |
| 🟡 黃燈 | `#E6A817` | `#fffcf0` | 猶豫、沉沒成本 |
| 🟡ₚ 被動黃燈 | `#9B59B6` | `#f9f0ff` | 被送來、洗腦最深，用紫色區分 |
| 🟢 綠燈 | `#28a745` | `#f0fff4` | 主動懷疑、已知被騙 |

---

## 七、15組腳本對應關係

| 燈號 | 嗔（假檢警） | 貪（投資） | 癡（感情） | 傲（優越） | 疑（懷疑） |
|------|-------------|-----------|-----------|-----------|-----------|
| 🔴紅 | script-red-chen.html | script-red-tan.html | script-red-chi.html | script-red-ao.html | script-red-yi.html |
| 🟡黃 | script-yellow-chen.html | script-yellow-tan.html | script-yellow-chi.html | script-yellow-ao.html | script-yellow-yi.html |
| 🟢綠 | script-green-chen.html | script-green-tan.html | script-green-chi.html | script-green-ao.html | script-green-yi.html |

> **被動型黃燈（🟡ₚ）**：不額外建頁面，在對應的黃燈腳本頁內以分頁方式呈現，切換標籤即可。

---

## 八、建置優先順序與分工建議

### Phase 1（核心骨架）
- [ ] `style.css` 完整樣式
- [ ] `index.html` 首頁
- [ ] `system.html` 系統框架（含三問互動）
- [ ] `matrix.html` 腳本矩陣

### Phase 2（腳本模板）
- [ ] `data/scripts.js` 資料結構（空殼，先填紅燈×嗔）
- [ ] `script-red-chen.html` 完整模板（含節點切換 + 版本切換 JS）
- [ ] 確認模板功能正確後，複製製作其餘14頁

### Phase 3（話術填入）
- [ ] 按照原始文件，將15組腳本 × 8節點 × 5版本的話術逐一填入 `data/scripts.js`
- [ ] 重點優先：紅燈系列（3組）→ 黃燈系列 → 綠燈系列

### Phase 4（測驗與查詢）
- [ ] `quiz.html` + 30題題庫
- [ ] `quickref.html` 快速查詢卡

---

## 九、與現有網站的整合方式

現有網站：https://fanciful-pavlova-0d7a69.netlify.app/

**方案A（獨立部署）**：新訓練平台作為獨立 Netlify 站台，在現有網站的導覽列加入「進階訓練」連結。

**方案B（整合）**：將新平台的 HTML 檔案直接加入現有網站的 zip 壓縮包，共用 `style.css` 色彩變數，在現有網站導覽列加入新入口。

> 建議：**先採方案A（獨立）**，內容穩定後再整合，避免影響現有網站運作。

---

## 十、附錄：節點說明快查

| 節點 | 名稱 | 核心目的 |
|------|------|----------|
| 節點1 | 情境判斷問句 | 確認行為狀態（通話中/等回撥/正在操作） |
| 節點2A | 依附程度判斷 | 判斷掛電話或靜音策略 |
| 節點2B | 最佳介入時機 | 對方等回撥時，引導個案 |
| 節點2C | 緊急止損 | 正在操作時立即中止 |
| 節點3 | 穩定化 | 打破孤立感、解除時間壓力 |
| 節點4 | 偵測保密要求 | 找到疑點、植入懷疑 |
| 節點5 | 引導自我發現（SCID式） | 讓個案自己說出矛盾 |
| 節點6 | 個案不配合應對 | 處理拒絕、指控、沉默 |
| 節點7 | 守（穩住決定後） | 接住羞愧感、預告後續心理反應 |
| 節點8 | 自傷風險篩檢（全程嵌入） | 在任何節點中偵測高風險 |

---

*本文件由 Claude（Anthropic）依據田心喬醫師提供的「165AI_v2_全腳本_修正版.docx」生成*
*建置完成後請部署至 Netlify 並更新既有網站連結*
