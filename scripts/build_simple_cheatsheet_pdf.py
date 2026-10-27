import os
import subprocess
import fitz

WORKSPACE = r"C:\Users\user\Desktop\新增資料夾 (2)\安基作業教學_20260819"
HTML_OUT = os.path.join(WORKSPACE, "cheatsheet_temp.html")
OLD_PDF = os.path.join(WORKSPACE, "安基作業教學_專職極簡懶人卡_A4大字版.pdf")
PDF_OUT = os.path.join(WORKSPACE, "安基作業教學_專職實務速查卡_A4大字版.pdf")
ARTIFACT_DIR = r"C:\Users\user\.gemini\antigravity-cli\brain\6a8645fc-0948-406d-9953-44608fc35fad"

if os.path.exists(OLD_PDF):
    try:
        os.remove(OLD_PDF)
    except OSError:
        pass

HTML_CONTENT = r"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<title>安基作業 專職實務操作速查卡 (A4雙面大字版)</title>
<style>
  @page {
    size: A4 portrait;
    margin: 7mm 8.5mm;
  }
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }
  body {
    font-family: "Microsoft JhengHei", "PingFang TC", sans-serif;
    color: #0f172a;
    background: #fff;
    font-size: 10pt;
    line-height: 1.34;
  }
  .page {
    width: 100%;
    height: 281mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    page-break-after: always;
  }
  .page:last-child {
    page-break-after: auto;
  }

  /* Header */
  .header {
    background: #1e293b;
    color: #fff;
    padding: 7px 14px;
    border-radius: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
  }
  .header h1 {
    font-size: 14pt;
    font-weight: 900;
    letter-spacing: 0.3px;
    white-space: nowrap;
  }
  .header .sub {
    font-size: 9.2pt;
    background: #f59e0b;
    color: #0f172a;
    font-weight: 900;
    padding: 3px 10px;
    border-radius: 99px;
    white-space: nowrap;
    flex-shrink: 0;
  }

  /* Golden Rule Banner */
  .golden-banner {
    background: #fef2f2;
    border: 2.5px solid #dc2626;
    border-radius: 8px;
    padding: 6px 12px;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .golden-banner .icon {
    font-size: 17pt;
    font-weight: 900;
    color: #dc2626;
    flex-shrink: 0;
  }
  .golden-banner .text {
    font-size: 10.2pt;
    font-weight: 800;
    color: #7f1d1d;
  }
  .golden-banner .text b {
    color: #dc2626;
    text-decoration: underline;
  }

  /* Section Box */
  .sec-box {
    border: 2px solid #cbd5e1;
    border-radius: 8px;
    background: #fff;
  }
  .sec-title {
    background: #0f172a;
    color: #fff;
    padding: 5px 12px;
    font-size: 11pt;
    font-weight: 900;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
  }
  .sec-title.blue { background: #1d4ed8; }
  .sec-title.green { background: #047857; }
  .sec-title.purple { background: #6d28d9; }
  .sec-title.amber { background: #b45309; }
  .sec-title.red { background: #b91c1c; }

  .sec-title span.badge {
    font-size: 8.8pt;
    background: rgba(255,255,255,0.22);
    padding: 1px 8px;
    border-radius: 99px;
    font-weight: 700;
    white-space: nowrap;
    flex-shrink: 0;
  }

  .sec-body {
    padding: 7px 9px;
    background: #fff;
    border-bottom-left-radius: 6px;
    border-bottom-right-radius: 6px;
  }

  /* 3-Column Payment Grid */
  .pay-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1.16fr;
    gap: 7px;
  }
  .pay-card {
    border: 2px solid #94a3b8;
    border-radius: 7px;
    padding: 7px 8px;
    background: #f8fafc;
    display: flex;
    flex-direction: column;
    gap: 5px;
  }
  .pay-card.cash { border-color: #16a34a; background: #f0fdf4; }
  .pay-card.res { border-color: #2563eb; background: #eff6ff; }
  .pay-card.pay { border-color: #dc2626; background: #fff1f2; }

  .pay-head {
    font-size: 10.5pt;
    font-weight: 900;
    padding-bottom: 4px;
    border-bottom: 1.5px solid rgba(0,0,0,0.12);
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 4px;
  }
  .pay-head .tag {
    font-size: 8.2pt;
    padding: 1px 6px;
    border-radius: 4px;
    white-space: nowrap;
    flex-shrink: 0;
  }
  .pay-card.cash .pay-head { color: #166534; }
  .pay-card.cash .pay-head .tag { background: #dcfce7; color: #166534; border: 1px solid #86efac; }
  .pay-card.res .pay-head { color: #1e40af; }
  .pay-card.res .pay-head .tag { background: #dbeafe; color: #1e40af; border: 1px solid #93c5fd; }
  .pay-card.pay .pay-head { color: #991b1b; }
  .pay-card.pay .pay-head .tag { background: #dc2626; color: #fff; }

  .step-list {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  .step-list li {
    font-size: 9.6pt;
    font-weight: 700;
    display: flex;
    gap: 5px;
    align-items: flex-start;
  }
  .step-num {
    background: #1e293b;
    color: #fff;
    font-size: 8.5pt;
    font-weight: 900;
    min-width: 17px;
    height: 17px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    margin-top: 1px;
    flex-shrink: 0;
  }
  .pay-card.cash .step-num { background: #16a34a; }
  .pay-card.res .step-num { background: #2563eb; }
  .pay-card.pay .step-num { background: #dc2626; }

  .stop-pill {
    background: #dc2626;
    color: #fff;
    font-weight: 900;
    padding: 0px 5px;
    border-radius: 4px;
    font-size: 8.8pt;
    white-space: nowrap;
  }
  .sys-pill {
    background: #fef08a;
    color: #854d0e;
    border: 1px solid #eab308;
    font-weight: 900;
    padding: 0px 5px;
    border-radius: 4px;
    font-size: 8.8pt;
    white-space: nowrap;
  }

  /* Flow Steps Horizontal / Vertical */
  .flow-table {
    width: 100%;
    border-collapse: collapse;
  }
  .flow-table th, .flow-table td {
    border: 1.5px solid #cbd5e1;
    padding: 4.5px 8px;
    text-align: left;
    vertical-align: middle;
    font-size: 9.5pt;
    line-height: 1.32;
  }
  .flow-table th {
    background: #f1f5f9;
    font-weight: 900;
    color: #1e293b;
    width: 23%;
  }
  .flow-table td {
    font-weight: 700;
  }

  /* Two column layout */
  .two-col {
    display: grid;
    grid-template-columns: 1.05fr 0.95fr;
    gap: 8px;
  }

  /* Big Warning Callout */
  .warn-strip {
    background: #fffbeb;
    border: 1.5px solid #f59e0b;
    border-radius: 6px;
    padding: 5px 9px;
    font-size: 9.4pt;
    font-weight: 800;
    color: #92400e;
    margin-top: 6px;
  }
  .danger-strip {
    background: #fef2f2;
    border: 1.5px solid #ef4444;
    border-radius: 6px;
    padding: 5px 9px;
    font-size: 9.3pt;
    font-weight: 800;
    color: #991b1b;
    margin-top: 6px;
  }

  /* FAQ Table */
  .faq-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 5px;
  }
  .faq-item {
    border: 1.5px solid #fca5a5;
    background: #fff5f5;
    border-radius: 6px;
    padding: 4.5px 7px;
  }
  .faq-q {
    font-size: 9.4pt;
    font-weight: 900;
    color: #b91c1c;
    margin-bottom: 1.5px;
  }
  .faq-a {
    font-size: 9pt;
    font-weight: 700;
    color: #1e293b;
    line-height: 1.28;
  }

  .footer {
    text-align: center;
    font-size: 8.5pt;
    color: #64748b;
    font-weight: 700;
    border-top: 1px solid #cbd5e1;
    padding-top: 3px;
  }
</style>
</head>
<body>

<!-- ==================== PAGE 1: 正面 (新加保 + 續保 + 修改資料) ==================== -->
<div class="page">
  <div class="header">
    <h1>📋 安基互助基金 ── 專職人員實務操作速查卡（正面）</h1>
    <div class="sub">桌面常備・跨系統流程對照</div>
  </div>

  <div class="golden-banner">
    <div class="icon">🛑</div>
    <div class="text">
      全系統審核原則：每當完成「新增、修改、確認、請款」後，<b>均需請【主管】進入「審核作業」點選審核通過</b>，方可進行下一階段作業（若由主管親自建檔，亦需進入審核作業執行審核）。
    </div>
  </div>

  <!-- 任務一：新加保 -->
  <div class="sec-box">
    <div class="sec-title blue">
      <span>壹、社員【新加保】作業流程（依社員繳費方式選擇對應欄位）</span>
      <span class="badge">簡報 P.13~P.41、P.112~P.124</span>
    </div>
    <div class="sec-body">
      <div class="pay-grid">
        <!-- 1. 現金 -->
        <div class="pay-card cash">
          <div class="pay-head">
            <span>💵 方式 A：現場付現金</span>
            <span class="tag">標準流程</span>
          </div>
          <ul class="step-list">
            <li><span class="step-num">1</span><span>收妥社員現金，並請社員於要保書簽名。</span></li>
            <li><span class="step-num">2</span><span>進<b>【安基系統 ➔ 互助基金 ➔ 要保申請】</b>點選右上方「新增」。</span></li>
            <li><span class="step-num">3</span><span>輸入身分證、勾選產品、填寫受益人與體況告知，按「儲存」。</span></li>
            <li><span class="step-num">4</span><span>繳款方式選<b>「現金」</b>➔ 按<b>「確認」</b>。</span></li>
            <li><span class="step-num">5</span><span><span class="stop-pill">🛑 請主管審核</span> 請主管至<b>【互助基金 ➔ 審核作業】</b>審核通過。</span></li>
            <li><span class="step-num">6</span><span>至<b>【查詢作業】</b>確認狀態變更為<b>「待要保合併」</b>即完成收件。</span></li>
          </ul>
        </div>

        <!-- 2. 備轉金 -->
        <div class="pay-card res">
          <div class="pay-head">
            <span>🏦 方式 B：扣社員備轉金</span>
            <span class="tag">需確認餘額</span>
          </div>
          <ul class="step-list">
            <li><span class="step-num">1</span><span>先確認社員「備轉金帳戶」可用餘額是否足夠扣款。</span></li>
            <li><span class="step-num">2</span><span>進<b>【安基系統 ➔ 互助基金 ➔ 要保申請】</b>點選右上方「新增」。</span></li>
            <li><span class="step-num">3</span><span>輸入身分證、勾選產品、填寫受益人與體況告知，按「儲存」。</span></li>
            <li><span class="step-num">4</span><span>繳款方式選<b>「備轉金」</b>➔ 勾選下方明細 ➔ 按<b>「確認」</b>。</span></li>
            <li><span class="step-num">5</span><span><span class="stop-pill">🛑 請主管審核</span> 請主管至<b>【互助基金 ➔ 審核作業】</b>審核通過（系統自動扣減備轉金）。</span></li>
            <li><span class="step-num">6</span><span>至<b>【查詢作業】</b>確認狀態變更為<b>「待要保合併」</b>即完成。</span></li>
          </ul>
        </div>

        <!-- 3. 應付代收 -->
        <div class="pay-card pay">
          <div class="pay-head">
            <span>🔄 方式 C：應付代收</span>
            <span class="tag">⚠️ 需先開立傳票</span>
          </div>
          <ul class="step-list">
            <li><span class="step-num">1</span><span><span class="sys-pill">先至會計作業</span> 進<b>【會計作業 ➔ 開立傳票】</b>新增（轉帳支出），將保費轉入<b>「應付代收款-安基」</b>（借：依需求選科目 ／ 貸：代收互助基金），摘要填社員姓名。</span></li>
            <li><span class="step-num">2</span><span><span class="stop-pill">🛑 主管審核 1</span> 請主管至<b>【會計作業 ➔ 審核作業】</b>審過此傳票（審過後安基結餘才會顯示金額）。</span></li>
            <li><span class="step-num">3</span><span><span class="sys-pill">切回安基系統</span> 進<b>【互助基金 ➔ 要保申請】</b>新增要保書並按儲存。</span></li>
            <li><span class="step-num">4</span><span>繳款選<b>「應付代收」</b>➔ 勾選剛才轉入之明細 ➔ 按<b>「確認」</b>。</span></li>
            <li><span class="step-num">5</span><span><span class="stop-pill">🛑 主管審核 2</span> 請主管至<b>【互助基金 ➔ 審核作業】</b>審核通過。</span></li>
            <li><span class="step-num">6</span><span><span class="sys-pill">返回會計作業</span> 進<b>【開立傳票】</b>將系統產生之「轉帳傳票」按<b>確認</b> ➔ <span class="stop-pill">🛑 主管審核 3</span> 至<b>【會計審核】</b>審過即完成入帳。</span></li>
          </ul>
        </div>
      </div>
      <div class="warn-strip">
        💡 <b>新加保實務提醒：</b>① 若同一社員「當日加保 2 張以上」，每張保單均需各自獨立完成上述流程。 ② 於「待要保合併」前若需更正資料，可至【要保申請】直接點選「修改」或「作廢」（完成後亦需請主管審核）。
      </div>
    </div>
  </div>

  <!-- 任務二：年度續保 與 修改社員資料 -->
  <div class="two-col">
    <div class="sec-box">
      <div class="sec-title green">
        <span>貳、【年度續保】作業流程</span>
        <span class="badge">簡報 P.81~P.106</span>
      </div>
      <div class="sec-body">
        <ul class="step-list">
          <li><span class="step-num">1</span><span>進<b>【互助基金 ➔ 續保作業】</b>，篩選狀態<b>「續保中」</b>，檢視當年度續保名單與金額。</span></li>
          <li><span class="step-num">2</span><span>若社員<b>「本年度不續保」</b>：勾選該筆 ➔ 按<b>「不續保」</b>➔ <span class="stop-pill">🛑 請主管審核</span> 至審核作業審過。</span></li>
          <li><span class="step-num">3</span><span>若以<b>「應付代收」</b>繳納續保費：同樣<b>先至【會計作業】開立傳票並請主管審過</b>，再返回續保作業。</span></li>
          <li><span class="step-num">4</span><span>勾選續保社員 ➔ 選擇繳款方式（現金 / 備轉金 / 應付代收）➔ 按<b>「確認」</b>。</span></li>
          <li><span class="step-num">5</span><span><span class="stop-pill">🛑 請主管審核</span> 請主管至<b>【互助基金 ➔ 審核作業】</b>審過（若用應付代收，需再回會計確認傳票並請主管審過）。</span></li>
          <li><span class="step-num">6</span><span>審過後狀態變更為<b>「待續保合併」</b>，後續流程與新加保相同（合併作業 ➔ 送協會 ➔ 請款）。</span></li>
        </ul>
      </div>
    </div>

    <div class="sec-box">
      <div class="sec-title purple">
        <span>參、變更社員【受益人 / 地址電話】</span>
        <span class="badge">簡報 P.107~P.111</span>
      </div>
      <div class="sec-body">
        <table class="flow-table">
          <tr>
            <th>變更地址、電話</th>
            <td>請直接至<b>【社員系統】</b>修改，修改後<b>隔日</b>安基系統即會自動同步更新。</td>
          </tr>
          <tr>
            <th>變更受益人、<br>指定聯絡人</th>
            <td>
              1. 進<b>【互助基金 ➔ 基本資料】</b>查詢該名社員<br>
              2. 切換至「基金基本資料」或「有效基金」頁籤<br>
              3. 點選<b>「修改」</b>更新資料並按確認<br>
              4. <span class="stop-pill">🛑 請主管審核</span> 請主管至<b>【審核作業】</b>審核通過即生效。
            </td>
          </tr>
        </table>
        <div class="danger-strip">
          ⚠️ <b>備註：</b>基本資料之「要保紀錄」與「帳戶價值」僅供查詢；當年度保費與投保年齡上限請至<b>【產品設定】</b>查閱。
        </div>
      </div>
    </div>
  </div>

  <div class="footer">
    第 1 頁 / 共 2 頁（正面：新加保 3 大收款流程、年度續保、資料變更） ── 電腦版可開啟 index.html 使用「專職實務操作引導系統」逐步對照畫面操作
  </div>
</div>

<!-- ==================== PAGE 2: 背面 (合併送件 + 請款 + 協會核保沖銷 + 常見問題 FAQ) ==================== -->
<div class="page">
  <div class="header">
    <h1>📦 安基互助基金 ── 專職人員實務操作速查卡（背面）</h1>
    <div class="sub">收款後流程：合併送件 ➔ 請款匯款 ➔ 協會核保結案</div>
  </div>

  <!-- 任務四：合併作業與請款 -->
  <div class="sec-box">
    <div class="sec-title amber">
      <span>肆、收款完成後：【合併送協會 ＋ 請款匯款】流程（新加保、續保皆適用）</span>
      <span class="badge">簡報 P.42~P.61、P.89~P.101</span>
    </div>
    <div class="sec-body">
      <table class="flow-table">
        <tr>
          <th>步驟 ①：合併名冊<br><span style="font-size:8.3pt;color:#64748b;">【互助基金 ➔ 合併作業】</span></th>
          <td>
            1. 進<b>【合併作業】</b>，篩選<b>「待要保合併」</b>（續保則選「待續保合併」）。<br>
            2. <b>勾選</b>本次欲一併送件之社員名單（可多筆勾選）➔ 按右上方<b>「合併」</b>產生合併批號。<br>
            3. <span class="stop-pill">🛑 請主管審核 1</span> 請主管至<b>【互助基金 ➔ 審核作業】</b>審核通過，狀態將變更為<b>「已合併」</b>。
          </td>
        </tr>
        <tr>
          <th>步驟 ②：送至協會<br><span style="font-size:8.3pt;color:#64748b;">【互助基金 ➔ 合併作業】</span></th>
          <td>
            1. 返回<b>【合併作業】</b>，篩選狀態<b>「已合併」</b> ➔ 點開該批號按<b>「列印」</b>印出要保書/名冊，連同紙本簽名文件寄送協會。<br>
            2. 於畫面勾選該批號 ➔ 點選<b>「送協會」</b>。<br>
            3. <span class="stop-pill">🛑 請主管審核 2</span> 請主管至<b>【互助基金 ➔ 審核作業】</b>審核通過，狀態將變更為<b>「已送協會」</b>。
          </td>
        </tr>
        <tr>
          <th>步驟 ③：請款與傳票確認<br><span style="font-size:8.3pt;color:#64748b;">【合併作業 ➔ 會計作業】</span></th>
          <td>
            1. 返回<b>【合併作業】</b>，篩選<b>「已送協會」</b>➔ 勾選該批號 ➔ 點選<b>「請款」</b>。<br>
            2. <span class="stop-pill">🛑 請主管審核 3</span> 請主管至<b>【互助基金 ➔ 審核作業】</b>審過請款（系統將自動拋轉傳票至會計作業）。<br>
            3. <span class="sys-pill">切換至會計作業</span> 進<b>【會計作業 ➔ 開立傳票】</b>選取該張請款傳票，點進按<b>「確認」</b>。<br>
            4. <span class="stop-pill">🛑 請主管審核 4</span> 請主管至<b>【會計作業 ➔ 審核作業】</b>審過傳票 ➔ 由出納辦理匯款予安基協會。
          </td>
        </tr>
      </table>
    </div>
  </div>

  <!-- 任務五：協會核保通過後自動沖銷結案 -->
  <div class="sec-box">
    <div class="sec-title green">
      <span>伍、協會通知「核保通過 / 不通過」後：【自動沖銷結案】流程</span>
      <span class="badge">簡報 P.62~P.80、P.102~P.106</span>
    </div>
    <div class="sec-body">
      <table class="flow-table">
        <tr>
          <th>情況 A：全數核保通過<br><span style="color:#15803d;font-size:8.5pt;">（標準結案流程）</span></th>
          <td>
            1. 進<b>【互助基金 ➔ 合併作業】</b>，點開該批號確認全數為「通過」，點選<b>「核保通過」</b>。<br>
            2. <span class="stop-pill">🛑 請主管審核 1</span> 請主管至<b>【互助基金 ➔ 審核作業】</b>審過（系統將自動拋出沖銷傳票至會計作業）。<br>
            3. <span class="sys-pill">切換至會計作業</span> 進<b>【會計作業 ➔ 開立傳票】</b>選取自動沖銷傳票並按<b>「確認」</b>。<br>
            4. <span class="stop-pill">🛑 請主管審核 2</span> 請主管至<b>【會計作業 ➔ 審核作業】</b>審過傳票 ➔ <b>全案正式生效結案。</b>
          </td>
        </tr>
        <tr>
          <th>情況 B：部分或全部不通過<br><span style="color:#b91c1c;font-size:8.5pt;">（退件或退費處理）</span></th>
          <td>
            1. 進<b>【合併作業】</b>點開該批號，將未通過人員改選<b>「不通過」</b>（或整批點選「核保不通過」）。<br>
            2. <span class="stop-pill">🛑 請主管審核</span> 請主管至<b>【互助基金 ➔ 審核作業】</b>審過。<br>
            3. <span class="sys-pill">切換至會計作業</span> 進<b>【會計作業 ➔ 開立傳票】</b>確認沖銷/退費傳票 ➔ <span class="stop-pill">🛑 請主管審核</span> 審過會計傳票並辦理退費。
          </td>
        </tr>
      </table>
    </div>
  </div>

  <!-- 任務六：常見問題排除 FAQ -->
  <div class="sec-box">
    <div class="sec-title red">
      <span>💡 陸、常見問題排除指南（6 大跨系統檢核要點）</span>
      <span class="badge">實務常見狀況與處理方式</span>
    </div>
    <div class="sec-body">
      <div class="faq-grid">
        <div class="faq-item">
          <div class="faq-q">Q1：點選確認後，為什麼畫面持續停留在「待審核」無法進行下一步？</div>
          <div class="faq-a">👉 需待<b>主管審核放行</b>。請通知主管至<b>【審核作業】</b>勾選並審核通過，重新整理畫面後即可進入下一階段。</div>
        </div>
        <div class="faq-item">
          <div class="faq-q">Q2：繳款選擇「應付代收」時，為什麼下方結餘顯示為 0、無法勾選？</div>
          <div class="faq-a">👉 請先至<b>【會計作業 ➔ 開立傳票】</b>開立轉帳傳票將款項轉入「代收互助基金」科目，並請<b>主管於會計作業審核通過</b>後，安基系統即會顯示結餘。</div>
        </div>
        <div class="faq-item">
          <div class="faq-q">Q3：已於安基點選「請款」或「核保通過」，為什麼會計帳務尚未入帳？</div>
          <div class="faq-a">👉 安基審核通過後會將傳票拋轉至會計系統，請<b>切換至【會計作業 ➔ 開立傳票】點選確認，並請主管審過會計傳票</b>即完成入帳。</div>
        </div>
        <div class="faq-item">
          <div class="faq-q">Q4：同一位社員當日同時投保 2 張互助基金，可否於同一筆建檔？</div>
          <div class="faq-a">👉 <b>需分開建檔。</b>請於【要保申請】分別新增 2 筆、各自確認繳款並請主管審核；待狀態皆為「待要保合併」後，再一併勾選合併。</div>
        </div>
        <div class="faq-item">
          <div class="faq-q">Q5：剛建檔之要保書發現資料有誤，或社員取消投保時該如何處理？</div>
          <div class="faq-a">👉 於合併送件前，可直接至<b>【要保申請】</b>選取該筆點選<b>「修改」或「作廢」</b>，完成後請主管至【審核作業】審過即可。</div>
        </div>
        <div class="faq-item">
          <div class="faq-q">Q6：社員欲變更電話或通訊地址，為什麼無法在安基系統內直接修改？</div>
          <div class="faq-a">👉 電話與地址係連動社員主檔，請直接至<b>【社員系統】</b>修改，修改後<b>隔日</b>安基系統即會自動同步更新。</div>
        </div>
      </div>
    </div>
  </div>

  <div class="footer">
    第 2 頁 / 共 2 頁（背面：合併送協會、請款匯款、核保自動沖銷結案、常見問題排除指南） ── 儲蓄互助社 專職人員實務操作速查卡
  </div>
</div>

</body>
</html>
"""

with open(HTML_OUT, "w", encoding="utf-8") as f:
    f.write(HTML_CONTENT)

chrome_paths = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]
browser = next((p for p in chrome_paths if os.path.exists(p)), None)
if not browser:
    raise RuntimeError("No Chrome/Edge found for PDF generation")

cmd = [
    browser,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={PDF_OUT}",
    HTML_OUT,
]
subprocess.run(cmd, check=True)

if os.path.exists(HTML_OUT):
    os.remove(HTML_OUT)

doc = fitz.open(PDF_OUT)
print(f"Generated {PDF_OUT} with {len(doc)} pages.")
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=150)
    out_png = os.path.join(ARTIFACT_DIR, f"cheatsheet_p{i+1}.png")
    pix.save(out_png)
    print(f"Saved preview: {out_png}")
doc.close()
