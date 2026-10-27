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
    font-size: 9.8pt;
    line-height: 1.33;
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
    font-size: 13.8pt;
    font-weight: 900;
    letter-spacing: 0.3px;
    white-space: nowrap;
  }
  .header .sub {
    font-size: 9pt;
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
    font-size: 16pt;
    font-weight: 900;
    color: #dc2626;
    flex-shrink: 0;
  }
  .golden-banner .text {
    font-size: 9.8pt;
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
    padding: 4.5px 12px;
    font-size: 10.6pt;
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
    font-size: 8.6pt;
    background: rgba(255,255,255,0.22);
    padding: 1px 8px;
    border-radius: 99px;
    font-weight: 700;
    white-space: nowrap;
    flex-shrink: 0;
  }

  .sec-body {
    padding: 6.5px 9px;
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
    padding: 6.5px 8px;
    background: #f8fafc;
    display: flex;
    flex-direction: column;
    gap: 4.5px;
  }
  .pay-card.cash { border-color: #16a34a; background: #f0fdf4; }
  .pay-card.res { border-color: #2563eb; background: #eff6ff; }
  .pay-card.pay { border-color: #dc2626; background: #fff1f2; }

  .pay-head {
    font-size: 10.2pt;
    font-weight: 900;
    padding-bottom: 4px;
    border-bottom: 1.5px solid rgba(0,0,0,0.12);
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 4px;
  }
  .pay-head .tag {
    font-size: 8pt;
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
    gap: 3.8px;
  }
  .step-list li {
    font-size: 9.3pt;
    font-weight: 700;
    display: flex;
    gap: 5px;
    align-items: flex-start;
  }
  .step-num {
    background: #1e293b;
    color: #fff;
    font-size: 8.2pt;
    font-weight: 900;
    min-width: 16px;
    height: 16px;
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
    font-size: 8.4pt;
    white-space: nowrap;
  }
  .sys-pill {
    background: #fef08a;
    color: #854d0e;
    border: 1px solid #eab308;
    font-weight: 900;
    padding: 0px 5px;
    border-radius: 4px;
    font-size: 8.4pt;
    white-space: nowrap;
  }

  /* Flow Steps Horizontal / Vertical */
  .flow-table {
    width: 100%;
    border-collapse: collapse;
  }
  .flow-table th, .flow-table td {
    border: 1.5px solid #cbd5e1;
    padding: 4px 8px;
    text-align: left;
    vertical-align: middle;
    font-size: 9.2pt;
    line-height: 1.3;
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
    grid-template-columns: 1.02fr 0.98fr;
    gap: 8px;
  }

  /* Big Warning Callout */
  .warn-strip {
    background: #fffbeb;
    border: 1.5px solid #f59e0b;
    border-radius: 6px;
    padding: 4.5px 9px;
    font-size: 9pt;
    font-weight: 800;
    color: #92400e;
    margin-top: 5px;
  }
  .danger-strip {
    background: #fef2f2;
    border: 1.5px solid #ef4444;
    border-radius: 6px;
    padding: 4.5px 9px;
    font-size: 9pt;
    font-weight: 800;
    color: #991b1b;
    margin-top: 5px;
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
    padding: 4px 7px;
  }
  .faq-q {
    font-size: 9.1pt;
    font-weight: 900;
    color: #b91c1c;
    margin-bottom: 1.5px;
  }
  .faq-a {
    font-size: 8.8pt;
    font-weight: 700;
    color: #1e293b;
    line-height: 1.26;
  }

  .footer {
    text-align: center;
    font-size: 8.4pt;
    color: #64748b;
    font-weight: 700;
    border-top: 1px solid #cbd5e1;
    padding-top: 3px;
  }
</style>
</head>
<body>

<!-- ==================== PAGE 1: 正面 (新加保 3 大付款方式 + 年度續保 + 調整加保資料) ==================== -->
<div class="page">
  <div class="header">
    <h1>📋 協會代辦互助基金（安基作業）── 專職人員實務操作速查卡（正面）</h1>
    <div class="sub">桌面常備・對應原簡報 P.1~P.133</div>
  </div>

  <div class="golden-banner">
    <div class="icon">🛑</div>
    <div class="text">
      跨系統核心檢核：完成「合併送件送審、應付代收/備轉金/沖銷傳票開立」後，<b>均需請【主管】進入「審核作業」點選審核通過</b>，下一階段按鈕或【傳票確認作業】才會顯示！（註：C 級社於合併送件時免等主管審核，P.68）
    </div>
  </div>

  <!-- 任務一：新加保 -->
  <div class="sec-box">
    <div class="sec-title blue">
      <span>壹、社員【新加保】作業流程（依社員繳交互助費方式選擇對應欄位）</span>
      <span class="badge">簡報 P.13~P.24、P.98~P.124</span>
    </div>
    <div class="sec-body">
      <div class="pay-grid">
        <!-- 1. 現金收款 -->
        <div class="pay-card cash">
          <div class="pay-head">
            <span>💵 付款 A：現金收款</span>
            <span class="tag">安基 ➔ 臨櫃收現</span>
          </div>
          <ul class="step-list">
            <li><span class="step-num">1</span><span>進<b>【安基作業 ➔ 協會代辦互助基金 ➔ 加保申請名冊】</b>點右上角<b>「＋」</b>新增 (P.9~13)。</span></li>
            <li><span class="step-num">2</span><span>選擇<b>「申請方案」</b>（年度、計畫）與<b>「申請人」</b>，填寫<b>「職業、職稱」</b>(P.14~17)。</span></li>
            <li><span class="step-num">3</span><span>選<b>「受益人分配方式」</b>並填明細，輸入補助金額與<b>「預計生效日」</b>(P.18~20)。</span></li>
            <li><span class="step-num">4</span><span>付款方式選<b>「現金收款」</b>➔ 先點<b>「暫存」</b>再按<b>「送出」</b>(P.22)。</span></li>
            <li><span class="step-num">5</span><span><span class="sys-pill">切換至臨櫃作業</span> 點<b>【社員搜尋】</b>輸入帳號並點<b>「選擇」</b>(P.98~101)。</span></li>
            <li><span class="step-num">6</span><span>進<b>【現金收款作業】</b>➔ <span class="stop-pill">🛑 移除無關項目</span> ➔ 點<b>「確認收款並列印收款單」</b>(P.102~106)。</span></li>
          </ul>
        </div>

        <!-- 2. 備轉金 -->
        <div class="pay-card res">
          <div class="pay-head">
            <span>🏦 付款 B：扣社員備轉金</span>
            <span class="tag">安基 ➔ 會計確認</span>
          </div>
          <ul class="step-list">
            <li><span class="step-num">1</span><span>進<b>【安基作業 ➔ 協會代辦互助基金 ➔ 加保申請名冊】</b>點右上角<b>「＋」</b>新增 (P.13)。</span></li>
            <li><span class="step-num">2</span><span>選擇<b>「申請方案」</b>與<b>「申請人」</b>，填寫<b>「職業、職稱」</b>及<b>「受益人、預計生效日」</b>(P.14~20)。</span></li>
            <li><span class="step-num">3</span><span>付款方式選<b>「備轉金」</b>（若有群組可選扣款成員），確認下方顯示<b>「結餘」</b>(P.23)。</span></li>
            <li><span class="step-num">4</span><span>先點<b>「暫存」</b>再按<b>「送出」</b>，系統自動產生備轉金轉帳傳票 (P.107)。</span></li>
            <li><span class="step-num">5</span><span><span class="sys-pill">切換至會計作業</span> 點左側<b>【傳票確認作業】</b>(P.108~109)。</span></li>
            <li><span class="step-num">6</span><span>（若查無傳票請主管至<b>【審核作業】</b>審過）找到傳票點<b>「通過並列印」</b>即完成 (P.110~111)。</span></li>
          </ul>
        </div>

        <!-- 3. 應付代收 -->
        <div class="pay-card pay">
          <div class="pay-head">
            <span>🔄 付款 C：應付代收</span>
            <span class="tag">⚠️ 先至會計開傳票</span>
          </div>
          <ul class="step-list">
            <li><span class="step-num">1</span><span><span class="sys-pill">① 先至會計作業</span> 進<b>【傳票管理 ➔ 開立傳票】</b>（支出轉帳傳票）點<b>「新增傳票項目」</b>(P.112~114)。</span></li>
            <li><span class="step-num">2</span><span><b>借方：</b>選<b>「社員」</b>輸入社員帳號、依實際需求選擇會計科目、輸入應繳金額、選<b>「借方」</b>確定 (P.115)。</span></li>
            <li><span class="step-num">3</span><span><b>貸方：</b>再點新增，同樣選<b>「社員」</b>輸入帳號、選<b>「其他會計科目 ➔ 代收互助基金(21514/21515)」</b>、同金額、選<b>「貸方」</b>➔ 按<b>「送出」</b>(P.116~119)。</span></li>
            <li><span class="step-num">4</span><span><span class="sys-pill">② 切回安基作業</span> 於加保畫面選<b>「應付代收」</b>，確認下方<b>「結餘」</b>有金額 ➔ 先點<b>「暫存」</b>再按<b>「送出」</b>(P.120)。</span></li>
            <li><span class="step-num">5</span><span><span class="sys-pill">③ 返回會計作業</span> 進<b>【傳票確認作業】</b>（待主管審過後）點<b>「通過並列印」</b>即完成 (P.121~124)。</span></li>
          </ul>
        </div>
      </div>
      <div class="warn-strip">
        💡 <b>新加保防呆要點：</b>① 受益人若指定僅 1 人，分配方式選「平均分配」或「依照順序」皆可 (P.19)。 ② 臨櫃現金收款時，務必將社員名下非本次互助基金的其他待繳項目點選<b>【移除】</b>(P.104)。
      </div>
    </div>
  </div>

  <!-- 任務二：年度續保 與 任務三：調整加保資料 / 基本資料查詢 -->
  <div class="two-col">
    <div class="sec-box">
      <div class="sec-title green">
        <span>貳、【年度續保】匯入續約名冊與批次送出</span>
        <span class="badge">簡報 P.25~P.31、P.45~P.47</span>
      </div>
      <div class="sec-body">
        <ul class="step-list">
          <li><span class="step-num">1</span><span>進<b>【安基作業 ➔ 協會代辦互助基金 ➔ 加保申請名冊】</b>，點選上方藍色<b>「匯入續約名冊」</b>按鈕 (P.27)。</span></li>
          <li><span class="step-num">2</span><span>於彈出視窗選擇欲續保之<b>「年度」</b>，再點選<b>「匯入」</b>(P.28)。</span></li>
          <li><span class="step-num">3</span><span>將本次要續約的社員名單<b>「打勾」</b>起來 (P.29)。</span></li>
          <li><span class="step-num">4</span><span>點選<b>「確認送出加保申請」</b>➔ 再點<b>「回到加保申請名冊」</b>(P.30~31)。</span></li>
          <li><span class="step-num">5</span><span>若需變更付款方式或受益人，請依右側「參、調整加保資料」步驟修改（單筆鉛筆修改或 Excel 批次匯出入）。</span></li>
          <li><span class="step-num">6</span><span>檢查列表中狀態為<b>「未送出」</b>之資料，勾選後點選上方<b>「批次送出」</b>，確認全數轉為<b>「已送出」</b>(P.45~47)。</span></li>
        </ul>
      </div>
    </div>

    <div class="sec-box">
      <div class="sec-title purple">
        <span>參、【調整加保資料】與查看基金基本資料</span>
        <span class="badge">簡報 P.4~P.8、P.32~P.44</span>
      </div>
      <div class="sec-body">
        <table class="flow-table">
          <tr>
            <th>單筆手動調整<br><span style="font-size:8pt;color:#64748b;">(P.32~P.37)</span></th>
            <td>於【加保申請名冊】點選該社員右側<b>「綠色鉛筆」</b>➔ 修改付款方式（如改為應付代收）或資料 ➔ <b>先點「暫存」再按「送出」</b>➔ 確認狀態變為<b>「已送出」</b>。</td>
          </tr>
          <tr>
            <th>多筆批次調整<br><span style="font-size:8pt;color:#64748b;">(P.38~P.44)</span></th>
            <td>
              1. 於【加保申請名冊】勾選多筆資料 ➔ 點<b>「匯出名冊」</b>下載 Excel<br>
              2. 於 Excel 將付款方式整批改為「應付代收」並存檔 (P.40~41)<br>
              3. 回系統點<b>「匯入名冊」</b>上傳該 Excel ➔ 勾選未送出資料按<b>「批次送出」</b>。
            </td>
          </tr>
        </table>
        <div class="danger-strip">
          🔍 <b>查資格與各計畫互助費 (P.4~P.8)：</b>進【協會代辦互助基金】點選該基金右側<b>「綠色鉛筆」</b>，即可查看【基本資料】年齡限制與【互助費與經辦費明細】。
        </div>
      </div>
    </div>
  </div>

  <div class="footer">
    第 1 頁 / 共 2 頁（正面：新加保 3 大付款流程、年度續保匯入、單筆與多筆資料調整） ── 電腦與手機可開啟 index.html 使用「專職實務操作引導系統」逐步對照紅框截圖
  </div>
</div>

<!-- ==================== PAGE 2: 背面 (合併送件 + 請款 + 協會核保沖銷 + 常見問題 FAQ) ==================== -->
<div class="page">
  <div class="header">
    <h1>📦 協會代辦互助基金（安基作業）── 專職人員實務操作速查卡（背面）</h1>
    <div class="sub">名冊建檔後：合併送件 ➔ 建立請款單 ➔ 自動沖銷結案</div>
  </div>

  <!-- 任務四：合併送件、送至協會與建立請款單 -->
  <div class="sec-box">
    <div class="sec-title amber">
      <span>肆、名冊狀態皆為「已送出」後：【預覽名冊 ➔ 合併送件 ➔ 送至協會 ➔ 建立請款單】</span>
      <span class="badge">簡報 P.48~P.80</span>
    </div>
    <div class="sec-body">
      <table class="flow-table">
        <tr>
          <th>步驟 ①：預覽與合併送件<br><span style="font-size:8pt;color:#64748b;">【加保申請名冊 P.48~58】</span></th>
          <td>
            1. 於<b>【加保申請名冊】</b>點左上角「☐」全選 ➔ 先點<b>「預覽名冊」</b>下載 PDF 詳加核對所有社員加保資料是否正確 (P.48~52)。<br>
            2. 確認無誤後，再次點左上角「☐」全選 ➔ 點選上方<b>「合併送件」</b>(P.54~57) ➔ 點左側選單進入<b>【加退保合併送件】</b>(P.58)。
          </td>
        </tr>
        <tr>
          <th>步驟 ②：送審查與送協會<br><span style="font-size:8pt;color:#64748b;">【加退保合併送件 P.59~70】</span></th>
          <td>
            1. 點該筆合併資料右側<b>「綠色鉛筆」</b>(P.59) ➔ 點<b>「列印名冊」</b>(P.60~62) 與<b>「產生繳費清單」</b>(P.63~65) 下載確認。<br>
            2. 點選<b>「確認名單，送主管審查」</b>，狀態變為「已送出審查」(P.66~67) ➔ <span class="stop-pill">🛑 請主管審核</span> 請主管至<b>【審核作業】</b>審過（C級社免等，P.68）。<br>
            3. 主管審過後，重新點進該筆【加退保合併送件】➔ 點選<b>「送至協會」</b>，狀態變為<b>「已送至協會」</b>(P.69~70)！
          </td>
        </tr>
        <tr>
          <th>步驟 ③：建立請款單與傳票<br><span style="font-size:8pt;color:#64748b;">【請款作業 ➔ 會計 P.71~80】</span></th>
          <td>
            1. 點選<b>「建立請款單」</b>自動跳至【請款作業】(P.72) ➔「1.請款單基本資料」選<b>【零用金】或【匯款】</b>填備註按<b>「下一步」</b>(P.73)。<br>
            2.「2.列印及輸入審查結果」點<b>「列印紙本請款單」</b>交主管簽核 ➔ 點<b>「上傳審核簽名後請款單」</b>➔ 審核結果勾選<b>「通過」</b>按<b>「送出」</b>(P.74)。<br>
            3.「3.會計開立傳票」點<b>「開立傳票」</b>(P.75)：借方（<code>11514 團體意外險墊款</code>）系統已自動帶出 (P.76)！請點<b>「新增傳票項目」</b>新增<b>貸方</b>：對象選<b>【社】</b>、依實際需求選擇會計科目（如 <code>110122 零用金</code>）、輸入總金額、選<b>【貸方】</b>按確定 (P.77) ➔ 點右下角<b>「送出」</b>並列印傳票 (P.78~80)。
          </td>
        </tr>
      </table>
    </div>
  </div>

  <!-- 任務五：協會核保通過後自動沖銷結案 -->
  <div class="sec-box">
    <div class="sec-title green">
      <span>伍、查看核保狀態與「加保通過」後：【自動沖銷結案 ＆ 檢視三張傳票】</span>
      <span class="badge">簡報 P.81~P.95、P.125~P.132</span>
    </div>
    <div class="sec-body">
      <table class="flow-table">
        <tr>
          <th>步驟 ①：查看核保狀態<br><span style="color:#15803d;font-size:8pt;">【帳務處理 P.81~86】</span></th>
          <td>
            進<b>【安基作業 ➔ 協會代辦互助基金 ➔ 帳務處理】</b>(P.81~83)：送件後核保狀態會先顯示為<b>「處理中」</b>(P.84)；請等待協會核保完成、狀態變更為<b>「加保通過」</b>後，即可執行自動沖銷 (P.85~86)。
          </td>
        </tr>
        <tr>
          <th>步驟 ②：執行自動沖銷<br><span style="color:#15803d;font-size:8pt;">【安基 ➔ 會計 P.87~95】</span></th>
          <td>
            1. 於<b>【帳務處理】</b>點左上角「☐」全選 ➔ 點上方<b>「自動沖銷」</b>➔ 於彈出視窗再點一次<b>「自動沖銷」</b>確認 (P.88~91)。<br>
            2. <span class="sys-pill">切換至會計作業</span> 進<b>【傳票確認作業】</b>（若無傳票請主管至【審核作業】審過），將系統自動產生的沖銷傳票全數點選<b>「通過」</b>(P.92~94)。<br>
            3. <span class="sys-pill">切回安基作業</span> 進<b>【帳務處理】</b>向右滑動底部橫條，確認「是否沖銷」欄位全部顯示為<b>「是」</b>即圓滿結案 (P.94~95)！
          </td>
        </tr>
        <tr>
          <th>補充：檢視三張傳票<br><span style="color:#475569;font-size:8pt;">【帳務處理 P.125~132】</span></th>
          <td>
            日後若需查閱傳票，可於<b>【帳務處理】</b>點選個別社員右側<b>「綠色鉛筆」</b>(P.126)，即可隨時點選檢視該社員之：①<b>收款傳票</b> (P.127~128)、②<b>墊付傳票</b> (P.129~130)、③<b>沖銷傳票</b>（借：21514 代收互助基金／貸：11514 墊款、41131 經辦收入，P.131~132）。
          </td>
        </tr>
      </table>
    </div>
  </div>

  <!-- 任務六：常見問題排除 FAQ -->
  <div class="sec-box">
    <div class="sec-title red">
      <span>💡 陸、常見問題排除指南（6 大跨系統實務檢核要點）</span>
      <span class="badge">簡報 P.24、P.66~P.69、P.104、P.133</span>
    </div>
    <div class="sec-body">
      <div class="faq-grid">
        <div class="faq-item">
          <div class="faq-q">Q1：為何在【會計作業 ➔ 傳票確認作業】找不到傳票？(P.133)</div>
          <div class="faq-a">👉 該張互助基金相關傳票尚未經主管放行。請通知<b>【主管】</b>切換至<b>【審核作業】</b>檢視並審核通過後，【傳票確認作業】即會出現該傳票。</div>
        </div>
        <div class="faq-item">
          <div class="faq-q">Q2：為何在【加退保合併送件】沒有顯示【送至協會】按鈕？(P.66~69)</div>
          <div class="faq-a">👉 點選【確認名單，送主管審查】後，需請<b>【主管】</b>至<b>【審核作業】</b>將該筆名單與相關傳票審核通過，重新進入後即會顯示【送至協會】（C級社除外）。</div>
        </div>
        <div class="faq-item">
          <div class="faq-q">Q3：付款方式選【應付代收】時，為何下方【結餘】顯示為 0？(P.24, 112)</div>
          <div class="faq-a">👉 代表尚未將款項轉入該互助基金。請先至<b>【會計作業 ➔ 開立傳票】</b>開立支出轉帳傳票（借貸方皆需選<b>社員並輸入帳號</b>，貸方選 21514/21515 代收互助基金）。</div>
        </div>
        <div class="faq-item">
          <div class="faq-q">Q4：名冊已經點選【送至協會】，事後發現有錯怎麼辦？(P.133)</div>
          <div class="faq-a">👉 點選【送至協會】後線上即鎖定無法退回。在核保通過前若要變更資料，<b>必須改送紙本向協會辦理（過程約需等待 1 個月）</b>，送出前務必先預覽名冊！</div>
        </div>
        <div class="faq-item">
          <div class="faq-q">Q5：臨櫃【現金收款作業】帶出多筆金額時，該如何處理？(P.103~104)</div>
          <div class="faq-a">👉 系統會一併帶出該社員名下其他待繳項目，請務必將「非本次代辦互助基金」的無關項目點選右側<b>【移除】</b>，再按確認收款並列印收款單。</div>
        </div>
        <div class="faq-item">
          <div class="faq-q">Q6：請款單在「3.會計開立傳票」時，借方需要手動新增嗎？(P.76~77)</div>
          <div class="faq-a">👉 <b>不需要！</b>借方（<code>11514 團體意外險墊款</code>）系統會自動帶出，您只需點【新增傳票項目】新增<b>貸方</b>（對象選<b>【社】</b>、依需求選科目如 110122 零用金）。</div>
        </div>
      </div>
    </div>
  </div>

  <div class="footer">
    第 2 頁 / 共 2 頁（背面：預覽與合併送件、送至協會、建立請款單、自動沖銷結案、常見問題排除指南） ── 儲蓄互助社 專職人員實務操作速查卡
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
