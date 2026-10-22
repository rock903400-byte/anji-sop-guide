# -*- coding: utf-8 -*-
"""
Generates a print-ready A4 portrait PDF summary manual:
`安基作業教學_SOP速查手冊_A4列印版.pdf`
from a dedicated print-optimized HTML template rendered via headless Chrome/Edge.
"""

import os
import subprocess
import tempfile
import fitz  # PyMuPDF for verification

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PDF = os.path.join(WORKSPACE_DIR, "安基作業教學_SOP速查手冊_A4列印版.pdf")

HTML_CONTENT = r"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8" />
  <title>安基作業（協會代辦互助基金）SOP 速查手冊</title>
  <style>
    @page {
      size: A4 portrait;
      margin: 10mm 11mm 10mm 11mm;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
    }

    body {
      font-family: "Microsoft JhengHei", "PingFang TC", "Noto Sans TC", sans-serif;
      color: #0f172a;
      background: #ffffff;
      font-size: 9.2pt;
      line-height: 1.42;
    }

    .page-break {
      page-break-before: always;
      break-before: page;
    }

    /* Header Banner */
    .doc-banner {
      background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
      color: #ffffff;
      padding: 10px 14px;
      border-radius: 7px;
      margin-bottom: 9px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .doc-banner h1 {
      font-size: 13.5pt;
      font-weight: 700;
      letter-spacing: 0.3px;
    }

    .doc-banner .sub {
      font-size: 8.2pt;
      color: #bfdbfe;
      margin-top: 2px;
    }

    .doc-banner .badge {
      background: #2563eb;
      border: 1px solid #60a5fa;
      color: #ffffff;
      font-size: 8pt;
      font-weight: 700;
      padding: 4px 9px;
      border-radius: 99px;
      text-align: right;
      white-space: nowrap;
    }

    /* Section Headings */
    .sec-h2 {
      font-size: 10.5pt;
      font-weight: 700;
      color: #1e3a8a;
      background: #eff6ff;
      border-left: 4px solid #1d4ed8;
      padding: 4px 9px;
      margin: 8px 0 6px 0;
      border-radius: 0 5px 5px 0;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .sec-h2 span.meta {
      font-size: 8pt;
      color: #475569;
      font-weight: 600;
    }

    /* Cross-System Swimlane Flow Box */
    .flow-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 7px;
      margin-bottom: 8px;
    }

    .flow-col {
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      background: #f8fafc;
      padding: 6px 7px;
    }

    .flow-col-title {
      font-size: 8.6pt;
      font-weight: 700;
      padding: 3px 7px;
      border-radius: 4px;
      margin-bottom: 5px;
      display: flex;
      justify-content: space-between;
    }

    .flow-step {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-left: 3px solid #2563eb;
      border-radius: 4px;
      padding: 3.5px 6px;
      margin-bottom: 4px;
      font-size: 8pt;
    }

    .flow-step:last-child {
      margin-bottom: 0;
    }

    .flow-step strong {
      color: #0f172a;
      display: inline;
    }

    .flow-step .p-ref {
      color: #1d4ed8;
      font-weight: 700;
      font-size: 7.5pt;
      float: right;
    }

    /* Module Badges */
    .mod {
      display: inline-block;
      font-size: 7.5pt;
      font-weight: 700;
      padding: 0.5px 5px;
      border-radius: 4px;
      margin-right: 3px;
      white-space: nowrap;
    }
    .mod-anji { background: #dbeafe; color: #1d4ed8; }
    .mod-counter { background: #ccfbf1; color: #0f766e; }
    .mod-acc { background: #ede9fe; color: #6d28d9; }
    .mod-claim { background: #fef3c7; color: #b45309; }
    .mod-mgr { background: #fee2e2; color: #b91c1c; }
    .mod-xls { background: #d1fae5; color: #047857; }

    .p-tag {
      display: inline-block;
      font-size: 7.4pt;
      font-weight: 700;
      color: #1e40af;
      background: #eff6ff;
      border: 1px solid #bfdbfe;
      padding: 0px 4px;
      border-radius: 3px;
      white-space: nowrap;
    }

    /* Comparison Table */
    table.comp-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 8.2pt;
      margin-bottom: 6px;
    }

    table.comp-table th,
    table.comp-table td {
      border: 1px solid #cbd5e1;
      padding: 5px 7px;
      vertical-align: top;
      text-align: left;
    }

    table.comp-table th {
      background: #f1f5f9;
      font-weight: 700;
      color: #0f172a;
    }

    .warn-text {
      color: #b91c1c;
      font-weight: 700;
    }

    /* Checklist Box */
    .phase-card {
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      margin-bottom: 7px;
      overflow: hidden;
      break-inside: avoid;
    }

    .phase-card-header {
      background: #f1f5f9;
      border-bottom: 1px solid #cbd5e1;
      padding: 4px 9px;
      font-size: 9pt;
      font-weight: 700;
      color: #0f172a;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .phase-card-note {
      background: #fffbeb;
      border-bottom: 1px solid #fde68a;
      padding: 3px 9px;
      font-size: 7.8pt;
      color: #92400e;
    }

    .chk-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 8.3pt;
    }

    .chk-table tr {
      border-bottom: 1px solid #e2e8f0;
    }

    .chk-table tr:last-child {
      border-bottom: none;
    }

    .chk-table td {
      padding: 4px 7px;
      vertical-align: top;
    }

    .chk-box {
      width: 22px;
      text-align: center;
      font-size: 10pt;
      line-height: 1;
      color: #475569;
      font-weight: 700;
    }

    .chk-step {
      width: 52px;
      font-weight: 700;
      color: #334155;
      white-space: nowrap;
      font-size: 7.9pt;
    }

    .chk-mod {
      width: 72px;
      white-space: nowrap;
    }

    .chk-pages {
      width: 82px;
      text-align: right;
      white-space: nowrap;
    }

    /* FAQ Box */
    .faq-box {
      border: 1px solid #cbd5e1;
      border-left: 4px solid #1d4ed8;
      border-radius: 5px;
      padding: 6px 9px;
      margin-bottom: 6px;
      background: #ffffff;
      break-inside: avoid;
    }

    .faq-box.warn { border-left-color: #d97706; background: #fffbeb; }
    .faq-box.danger { border-left-color: #dc2626; background: #fef2f2; }

    .faq-q {
      font-size: 8.8pt;
      font-weight: 700;
      color: #0f172a;
      margin-bottom: 2px;
      display: flex;
      justify-content: space-between;
    }

    .faq-a {
      font-size: 8.2pt;
      color: #334155;
    }

    .footer-note {
      margin-top: 6px;
      text-align: center;
      font-size: 7.5pt;
      color: #64748b;
      border-top: 1px solid #e2e8f0;
      padding-top: 4px;
    }
  </style>
</head>
<body>

  <!-- ==================== PAGE 1 ==================== -->
  <div class="doc-banner">
    <div>
      <h1>安基作業（協會代辦互助基金）SOP 標準作業速查手冊</h1>
      <div class="sub">原 133 頁教學簡報濃縮列印版｜跨系統流程導覽・三大付款方式對照・35 步防呆檢核清單</div>
    </div>
    <div class="badge">A4 濃縮速查版<br/>對應原簡報 P.1~P.133</div>
  </div>

  <div class="sec-h2">
    <span>一、全流程跨 5 大系統模組鳥瞰圖（依序由左至右、由上而下執行）</span>
    <span class="meta">核心關鍵：注意模組切換時機</span>
  </div>

  <div class="flow-grid">
    <div class="flow-col">
      <div class="flow-col-title mod-anji">
        <span>①【安基作業】建檔與送審</span>
        <span>P.4~70</span>
      </div>
      <div class="flow-step"><span class="p-ref">P.4~8</span><strong>0. 查看基金基本資料</strong><br/>確認投保資格限制、各計畫互助費與經辦費</div>
      <div class="flow-step"><span class="p-ref">P.9~24</span><strong>1A. 新加保單筆建檔</strong><br/>選方案、社員、受益人、預計生效日、付款方式</div>
      <div class="flow-step"><span class="p-ref">P.25~31</span><strong>1B. 續保匯入續約名冊</strong><br/>選年度匯入 ➔ 勾選續約社員 ➔ 確認送出申請</div>
      <div class="flow-step"><span class="p-ref">P.32~44</span><strong>2. 資料調整（可略）</strong><br/>單筆鉛筆修改，或多筆匯出 Excel 修改再匯入</div>
      <div class="flow-step"><span class="p-ref">P.45~52</span><strong>3. 批次送出＆預覽名冊</strong><br/>未送出勾選批次送出 ➔ 全選預覽 PDF 核對</div>
      <div class="flow-step"><span class="p-ref">P.53~67</span><strong>4. 合併送件＆送主管審查</strong><br/>全選合併送件 ➔ 列印名冊/繳費清單 ➔ 送審查</div>
    </div>

    <div class="flow-col">
      <div class="flow-col-title mod-counter">
        <span>②【臨櫃／會計】三種收款與確認</span>
        <span>P.96~124</span>
      </div>
      <div class="flow-step" style="border-left-color:#0f766e;"><span class="p-ref">P.98~106</span><strong>付款 A：現金收款（臨櫃作業）</strong><br/>社員搜尋 ➔ 現金收款作業 ➔ <strong>移除無關項目</strong> ➔ 確認收款並列印收款單</div>
      <div class="flow-step" style="border-left-color:#6d28d9;"><span class="p-ref">P.107~111</span><strong>付款 B：備轉金（會計作業）</strong><br/>安基選備轉金送出 ➔ 切換【會計作業】➔【傳票確認作業】➔ 通過並列印</div>
      <div class="flow-step" style="border-left-color:#dc2626;"><span class="p-ref">P.112~124</span><strong>付款 C：應付代收（先開傳票！）</strong><br/>① 先至【會計作業➔開立傳票】借：社員活期存款／貸：代收互助基金<br/>② 回【安基作業】確認有<strong>結餘</strong>後暫存並送出<br/>③ 再至【會計作業➔傳票確認作業】通過並列印</div>
      <div class="flow-step" style="border-left-color:#b91c1c;"><span class="p-ref">P.68, 133</span><strong>主管【審核作業】放行</strong><br/>主管審核合併送件名單與互助基金相關傳票</div>
    </div>

    <div class="flow-col">
      <div class="flow-col-title mod-claim">
        <span>③【請款／帳務】送協會與自動沖銷</span>
        <span>P.69~95</span>
      </div>
      <div class="flow-step"><span class="p-ref">P.69~70</span><strong>5. 點選【送至協會】</strong><br/>主管審核通過後，回加退保合併送件點選送至協會</div>
      <div class="flow-step" style="border-left-color:#b45309;"><span class="p-ref">P.71~80</span><strong>6. 建立請款單＆墊付傳票</strong><br/>選零用金/匯款 ➔ 紙本送審 ➔ 會計開立墊付傳票（借：意外險墊款／貸：零用金或銀行存款）</div>
      <div class="flow-step"><span class="p-ref">P.81~86</span><strong>7. 查看核保狀態（帳務處理）</strong><br/>等待狀態由「處理中」變為<strong>【加保通過】</strong></div>
      <div class="flow-step" style="border-left-color:#047857;"><span class="p-ref">P.87~95</span><strong>8. 自動沖銷＆會計傳票確認</strong><br/>安基帳務處理全選【自動沖銷】➔ 會計【傳票確認作業】通過 ➔ 回安基確認「是否沖銷=是」</div>
      <div class="flow-step"><span class="p-ref">P.125~132</span><strong>9. 帳務處理檢視三張傳票</strong><br/>可隨時點鉛筆檢視：收款傳票、墊付傳票、沖銷傳票</div>
    </div>
  </div>

  <div class="sec-h2">
    <span>二、三大付款方式跨系統操作對照表（新加保 P.21~24 ／ 補充說明 P.96~124）</span>
    <span class="meta">最常卡關重點！請依社員繳費方式對照執行</span>
  </div>

  <table class="comp-table">
    <thead>
      <tr>
        <th style="width:14%;">付款方式</th>
        <th style="width:21%;">適用情境與前置條件</th>
        <th style="width:45%;">跨系統標準操作順序（括號為原簡報頁碼）</th>
        <th style="width:20%;">防呆檢核重點</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>
          <span class="mod mod-counter">1. 現金收款</span><br/>
          <span class="p-tag">P.22</span> <span class="p-tag">P.98~106</span>
        </td>
        <td>
          <strong>社員現場／臨櫃繳現</strong><br/>
          無預收款時選用。直接於安基選擇【現金收款】暫存送出即可。
        </td>
        <td>
          ① <strong>【安基作業】</strong>付款方式選「現金收款」暫存並送出 (<span class="p-tag">P.22</span>)<br/>
          ② 切換至<strong>【臨櫃作業】</strong>➔ 點選【社員搜尋】輸入社員帳號並點【選擇】(<span class="p-tag">P.98~101</span>)<br/>
          ③ 點選【現金收款作業】，系統自動帶出代辦互助基金應繳金額 (<span class="p-tag">P.102~103</span>)<br/>
          ④ <span class="warn-text">將其他無關收款項目點選【移除】</span> (<span class="p-tag">P.104</span>)<br/>
          ⑤ 點選【確認收款並列印收款單】完成開立 (<span class="p-tag">P.105~106</span>)
        </td>
        <td>
          社員名下若有其他待繳項目會一併帶出，務必於 <span class="p-tag">P.104</span> <strong>移除非本次互助基金項目</strong>！
        </td>
      </tr>
      <tr>
        <td>
          <span class="mod mod-acc">2. 備轉金</span><br/>
          <span class="p-tag">P.23</span> <span class="p-tag">P.107~111</span>
        </td>
        <td>
          <strong>扣抵社員備轉金餘額</strong><br/>
          確認下方備轉金有結餘，於安基選【備轉金】暫存送出。
        </td>
        <td>
          ① <strong>【安基作業】</strong>付款方式選「備轉金」暫存並送出 (<span class="p-tag">P.23</span>, <span class="p-tag">P.107</span>)<br/>
          ② 點擊右上角切換至<strong>【會計作業】</strong>➔ 點選左側【傳票確認作業】(<span class="p-tag">P.108~109</span>)<br/>
          ③ 找到剛剛產生的傳票，點選【通過並列印】即顯示開立成功 (<span class="p-tag">P.110~111</span>)
        </td>
        <td>
          若【傳票確認作業】找不到該傳票，請主管先至【審核作業】放行 (<span class="p-tag">P.133</span>)。
        </td>
      </tr>
      <tr>
        <td>
          <span class="mod mod-acc">3. 應付代收</span><br/>
          <span class="p-tag">P.24</span> <span class="p-tag">P.112~124</span>
        </td>
        <td>
          <strong>由社員活存轉入代收</strong><br/>
          <span class="warn-text">必須先去【會計作業】開立支出轉帳傳票</span>，安基才會有結餘！
        </td>
        <td>
          ① 先切換至<strong>【會計作業】</strong>➔【傳票管理】➔【開立傳票】（支出轉帳傳票）(<span class="p-tag">P.112~113</span>)<br/>
          ② 點【新增傳票項目】輸入<strong>借方</strong>：選社員帳號、科目如 <code>11211 活期存款</code>、金額 (<span class="p-tag">P.114~115</span>)<br/>
          ③ 再點【新增傳票項目】輸入<strong>貸方</strong>：選對應代收科目（如 <code>21515 代收重大疾病互助基金</code> 或 <code>21514 代收社員意外互助基金</code>）、同金額 ➔ 點【送出】(<span class="p-tag">P.116~119</span>)<br/>
          ④ 回到<strong>【安基作業】</strong>確認下方【結餘】已顯示金額 ➔ 先點【暫存】再按【送出】(<span class="p-tag">P.120</span>)<br/>
          ⑤ 再次切換至<strong>【會計作業】</strong>➔【傳票確認作業】➔ 找到傳票點【通過並列印】(<span class="p-tag">P.121~124</span>)
        </td>
        <td>
          若安基下方【結餘】顯示 <code>0</code>，代表尚未開立轉帳傳票將費用轉到該互助基金 (<span class="p-tag">P.24</span>)。
        </td>
      </tr>
    </tbody>
  </table>

  <!-- ==================== PAGE 2 ==================== -->
  <div class="page-break"></div>

  <div class="sec-h2">
    <span>三、分階段標準作業檢核清單 — 階段一：介紹與新加保申請（P.4 ~ P.24）</span>
    <span class="meta">可於紙本「☐」直接打勾確認進度</span>
  </div>

  <div class="phase-card">
    <div class="phase-card-header">
      <span>1.1 查看互助基金基本資料與費率明細 ＆ 1.2 加保申請名冊功能介紹</span>
      <span class="p-tag">P.4 ~ P.12</span>
    </div>
    <table class="chk-table">
      <tr>
        <td class="chk-box">☐</td>
        <td class="chk-step">Step 1</td>
        <td class="chk-mod"><span class="mod mod-anji">安基作業</span></td>
        <td>點擊系統右上角【切換】➔ 點選【安基作業】，再點選左側選單【協會代辦互助基金】。</td>
        <td class="chk-pages"><span class="p-tag">P.4 ~ P.5</span></td>
      </tr>
      <tr>
        <td class="chk-box">☐</td>
        <td class="chk-step">Step 2</td>
        <td class="chk-mod"><span class="mod mod-anji">安基作業</span></td>
        <td>點選欲查看的互助基金（例：社員團體意外互助基金）右側「綠色鉛筆」圖示：於【基本資料】查看投保限制，於【互助費與經辦費明細】查看各計畫保額與費用。</td>
        <td class="chk-pages"><span class="p-tag">P.6 ~ P.8</span></td>
      </tr>
      <tr>
        <td class="chk-box">☐</td>
        <td class="chk-step">Step 3</td>
        <td class="chk-mod"><span class="mod mod-anji">安基作業</span></td>
        <td>點選左側【加保申請名冊】：右上角<strong>【＋】</strong>為新增加保；左上角<strong>【☐】</strong>為跨頁全選；勾選資料後點右上角<strong>【✕】</strong>為刪除。</td>
        <td class="chk-pages"><span class="p-tag">P.9 ~ P.12</span></td>
      </tr>
    </table>
  </div>

  <div class="phase-card">
    <div class="phase-card-header">
      <span>1.3 新加保單筆申請建檔流程</span>
      <span class="p-tag">P.13 ~ P.24</span>
    </div>
    <table class="chk-table">
      <tr>
        <td class="chk-box">☐</td>
        <td class="chk-step">Step 1</td>
        <td class="chk-mod"><span class="mod mod-anji">安基作業</span></td>
        <td>於【加保申請名冊】點選右上角【＋】開啟新加保視窗，選擇【申請方案】（保險年度如 115、子方案如計畫一）與【申請人】（選擇社員）。</td>
        <td class="chk-pages"><span class="p-tag">P.13 ~ P.15</span></td>
      </tr>
      <tr>
        <td class="chk-box">☐</td>
        <td class="chk-step">Step 2</td>
        <td class="chk-mod"><span class="mod mod-anji">安基作業</span></td>
        <td>確認系統自動帶出之社員基本資料，並填寫【職業】與【職稱】。</td>
        <td class="chk-pages"><span class="p-tag">P.16 ~ P.17</span></td>
      </tr>
      <tr>
        <td class="chk-box">☐</td>
        <td class="chk-step">Step 3</td>
        <td class="chk-mod"><span class="mod mod-anji">安基作業</span></td>
        <td>選擇【受益人分配方式】（法定繼承人／平均分配／依照順序）。選後兩者需填寫受益人資料；<strong>若指定受益人僅 1 人，選「平均分配」或「依照順序」皆可</strong>。</td>
        <td class="chk-pages"><span class="p-tag">P.18 ~ P.19</span></td>
      </tr>
      <tr>
        <td class="chk-box">☐</td>
        <td class="chk-step">Step 4</td>
        <td class="chk-mod"><span class="mod mod-anji">安基作業</span></td>
        <td>輸入【獎勵或補助／其他扣除金額】並選擇【預計生效日】。</td>
        <td class="chk-pages"><span class="p-tag">P.20</span></td>
      </tr>
      <tr>
        <td class="chk-box">☐</td>
        <td class="chk-step">Step 5</td>
        <td class="chk-mod"><span class="mod mod-anji">安基作業</span></td>
        <td>選擇【付款方式】（現金收款／備轉金／應付代收）。確認下方【結餘】有金額後，<strong>先點選【暫存】再按【送出】</strong>。</td>
        <td class="chk-pages"><span class="p-tag">P.21 ~ P.24</span></td>
      </tr>
    </table>
  </div>

  <div class="sec-h2">
    <span>階段二（上）：續保匯入、資料調整、批次送出與預覽名冊（P.25 ~ P.52）</span>
    <span class="meta">合併送件前之名單準備與檢核</span>
  </div>

  <div class="phase-card">
    <div class="phase-card-header">
      <span>2.1 續保流程 — 匯入續約名冊</span>
      <span class="p-tag">P.25 ~ P.31</span>
    </div>
    <table class="chk-table">
      <tr>
        <td class="chk-box">☐</td>
        <td class="chk-step">Step 1</td>
        <td class="chk-mod"><span class="mod mod-anji">安基作業</span></td>
        <td>於【加保申請名冊】點選上方【匯入續約名冊】按鈕，選擇續保【年度】後點選【匯入】。</td>
        <td class="chk-pages"><span class="p-tag">P.27 ~ P.28</span></td>
      </tr>
      <tr>
        <td class="chk-box">☐</td>
        <td class="chk-step">Step 2</td>
        <td class="chk-mod"><span class="mod mod-anji">安基作業</span></td>
        <td>勾選本次要續約的社員名單 ➔ 點選【確認送出加保申請】➔ 回到【加保申請名冊】檢視名單。</td>
        <td class="chk-pages"><span class="p-tag">P.29 ~ P.31</span></td>
      </tr>
    </table>
  </div>

  <div class="phase-card">
    <div class="phase-card-header">
      <span>2.2 調整資料（範例一：單筆手動調整 ／ 範例二：多筆匯出 Excel 修改再匯入）</span>
      <span class="p-tag">P.32 ~ P.44</span>
    </div>
    <div class="phase-card-note">💡 註：若資料無須調整可略過此步驟。以下示範將付款方式由「現金收款」更正為「應付代收」。</div>
    <table class="chk-table">
      <tr>
        <td class="chk-box">☐</td>
        <td class="chk-step">單筆調整</td>
        <td class="chk-mod"><span class="mod mod-anji">安基作業</span></td>
        <td>點選該社員右側「綠色鉛筆」圖示 (<span class="p-tag">P.32</span>) ➔ 將付款方式下拉改選為【應付代收】(<span class="p-tag">P.33~34</span>) ➔ <strong>先點【暫存】再按【送出】</strong>(<span class="p-tag">P.35</span>) ➔ 回到加保申請名冊確認狀態變為【已送出】(<span class="p-tag">P.36~37</span>)。</td>
        <td class="chk-pages"><span class="p-tag">P.32 ~ P.37</span></td>
      </tr>
      <tr>
        <td class="chk-box">☐</td>
        <td class="chk-step">多筆匯出</td>
        <td class="chk-mod"><span class="mod mod-anji">安基作業</span></td>
        <td>將欲修改的多筆資料勾選起來 (<span class="p-tag">P.38</span>) ➔ 點選【匯出名冊】，從右上角下載 Excel 檔案 (<span class="p-tag">P.39</span>)。</td>
        <td class="chk-pages"><span class="p-tag">P.38 ~ P.39</span></td>
      </tr>
      <tr>
        <td class="chk-box">☐</td>
        <td class="chk-step">多筆匯入</td>
        <td class="chk-mod"><span class="mod mod-xls">Excel批次</span></td>
        <td>打開 Excel 將付款方式由「現金收款」改為【應付代收】並存檔 (<span class="p-tag">P.40~41</span>) ➔ 回系統點選【匯入名冊】上傳修改後的 Excel (<span class="p-tag">P.42~43</span>)，顯示「儲存成功」(<span class="p-tag">P.44</span>)。</td>
        <td class="chk-pages"><span class="p-tag">P.40 ~ P.44</span></td>
      </tr>
    </table>
  </div>

  <div class="phase-card">
    <div class="phase-card-header">
      <span>2.3 批次送出與合併前預覽名冊</span>
      <span class="p-tag">P.45 ~ P.52</span>
    </div>
    <table class="chk-table">
      <tr>
        <td class="chk-box">☐</td>
        <td class="chk-step">Step 1</td>
        <td class="chk-mod"><span class="mod mod-anji">安基作業</span></td>
        <td>查看列表中「申請送出狀態」為【未送出】的資料，勾選後點選上方【批次送出】，確認狀態皆轉為【已送出】。</td>
        <td class="chk-pages"><span class="p-tag">P.45 ~ P.47</span></td>
      </tr>
      <tr>
        <td class="chk-box">☐</td>
        <td class="chk-step">Step 2</td>
        <td class="chk-mod"><span class="mod mod-anji">安基作業</span></td>
        <td>點擊左上角全選按鈕 <code>☐</code> 勾選全部資料 ➔ 點選【預覽名冊】➔ 開啟右上角下載的 PDF 檔案，詳加核對所有社員加保資料是否正確。</td>
        <td class="chk-pages"><span class="p-tag">P.48 ~ P.52</span></td>
      </tr>
    </table>
  </div>

  <!-- ==================== PAGE 3 ==================== -->
  <div class="page-break"></div>

  <div class="sec-h2">
    <span>階段二（下）：合併送件、主管審查、建立請款單與查看核保狀態（P.53 ~ P.86）</span>
    <span class="meta">送至協會前務必確認名冊無誤</span>
  </div>

  <div class="phase-card">
    <div class="phase-card-header">
      <span>2.4 合併送件與【加退保合併送件】主管審查、送至協會</span>
      <span class="p-tag">P.53 ~ P.70</span>
    </div>
    <div class="phase-card-note">⚠️ 警告：點選【送至協會】後若發現有錯，在核保通過前只能走「人工紙本變更」（需時約 1 個月），送出前務必確認名冊與繳費清單無誤！</div>
    <table class="chk-table">
      <tr>
        <td class="chk-box">☐</td>
        <td class="chk-step">Step 1</td>
        <td class="chk-mod"><span class="mod mod-anji">安基作業</span></td>
        <td>於【加保申請名冊】點擊全選按鈕 <code>☐</code> ➔ 點選【合併送件】(<span class="p-tag">P.54~56</span>)，跳出成功訊息後，點選左側選單【加退保合併送件】(<span class="p-tag">P.57~58</span>)。</td>
        <td class="chk-pages"><span class="p-tag">P.54 ~ P.58</span></td>
      </tr>
      <tr>
        <td class="chk-box">☐</td>
        <td class="chk-step">Step 2</td>
        <td class="chk-mod"><span class="mod mod-anji">安基作業</span></td>
        <td>點擊該筆合併送件資料的「綠色鉛筆」圖示 (<span class="p-tag">P.59</span>) ➔ 點選【列印名冊】下載確認資料 (<span class="p-tag">P.60~62</span>) ➔ 點選【產生繳費清單】下載確認社員繳費情形 (<span class="p-tag">P.63~65</span>)。</td>
        <td class="chk-pages"><span class="p-tag">P.59 ~ P.65</span></td>
      </tr>
      <tr>
        <td class="chk-box">☐</td>
        <td class="chk-step">Step 3</td>
        <td class="chk-mod"><span class="mod mod-mgr">主管審核</span></td>
        <td>點選【確認名單，送主管審查】，畫面顯示【已送出審查】(<span class="p-tag">P.66~67</span>) ➔ 請主管至【審核作業】完成審查 (<span class="p-tag">P.68</span>)。</td>
        <td class="chk-pages"><span class="p-tag">P.66 ~ P.68</span></td>
      </tr>
      <tr>
        <td class="chk-box">☐</td>
        <td class="chk-step">Step 4</td>
        <td class="chk-mod"><span class="mod mod-anji">安基作業</span></td>
        <td>主管審核通過後，回到【加退保合併送件】明細點選【送至協會】，畫面狀態變為【已送至協會】。</td>
        <td class="chk-pages"><span class="p-tag">P.69 ~ P.70</span></td>
      </tr>
    </table>
  </div>

  <div class="phase-card">
    <div class="phase-card-header">
      <span>2.5 建立請款單與會計開立墊付傳票 ＆ 2.6 查看核保狀態</span>
      <span class="p-tag">P.71 ~ P.86</span>
    </div>
    <table class="chk-table">
      <tr>
        <td class="chk-box">☐</td>
        <td class="chk-step">Step 1</td>
        <td class="chk-mod"><span class="mod mod-claim">請款作業</span></td>
        <td>於加退保合併送件點選【建立請款單】(<span class="p-tag">P.72</span>) ➔ 在「1.建立請款單」選【零用金】或【匯款】並填寫說明後按【下一步】(<span class="p-tag">P.73</span>) ➔ 在「2.列印紙本並輸入主管審查結果」列印送審並登錄結果 (<span class="p-tag">P.74</span>)。</td>
        <td class="chk-pages"><span class="p-tag">P.72 ~ P.74</span></td>
      </tr>
      <tr>
        <td class="chk-box">☐</td>
        <td class="chk-step">Step 2</td>
        <td class="chk-mod"><span class="mod mod-acc">會計作業</span></td>
        <td>在「3.會計開立傳票」點選【開立傳票】➔【新增傳票項目】，輸入墊付分錄（例：借方 <code>11514 團體意外險墊款</code>／貸方 <code>110122 零用金</code> 或銀行存款）➔ 借貸平衡後點【送出】並列印傳票。</td>
        <td class="chk-pages"><span class="p-tag">P.75 ~ P.80</span></td>
      </tr>
      <tr>
        <td class="chk-box">☐</td>
        <td class="chk-step">Step 3</td>
        <td class="chk-mod"><span class="mod mod-anji">安基作業</span></td>
        <td>切換回【安基作業 ➔ 協會代辦互助基金 ➔ 帳務處理】(<span class="p-tag">P.81~83</span>)，此時核保狀態為【處理中】(<span class="p-tag">P.84</span>)，等待協會核保完成變為<strong>【加保通過】</strong>(<span class="p-tag">P.85~86</span>)。</td>
        <td class="chk-pages"><span class="p-tag">P.81 ~ P.86</span></td>
      </tr>
    </table>
  </div>

  <div class="sec-h2">
    <span>階段三：加保通過後流程 — 自動沖銷與帳務處理三張傳票檢視（P.87 ~ P.95、P.125 ~ P.132）</span>
    <span class="meta">核保狀態變為「加保通過」後執行</span>
  </div>

  <div class="phase-card">
    <div class="phase-card-header">
      <span>3.1 自動沖銷與會計傳票確認 ＆ 3.2 帳務處理檢視三張傳票（收款／墊付／沖銷）</span>
      <span class="p-tag">P.87 ~ P.95, P.125 ~ P.132</span>
    </div>
    <table class="chk-table">
      <tr>
        <td class="chk-box">☐</td>
        <td class="chk-step">Step 1</td>
        <td class="chk-mod"><span class="mod mod-anji">安基作業</span></td>
        <td>於左側選單【帳務處理】先勾選全選，再點選上方【自動沖銷】(<span class="p-tag">P.88~89</span>)，於彈出視窗點選【自動沖銷】確認，跳出成功訊息 (<span class="p-tag">P.90~91</span>)。</td>
        <td class="chk-pages"><span class="p-tag">P.88 ~ P.91</span></td>
      </tr>
      <tr>
        <td class="chk-box">☐</td>
        <td class="chk-step">Step 2</td>
        <td class="chk-mod"><span class="mod mod-acc">會計作業</span></td>
        <td>切換至【會計作業 ➔ 傳票確認作業】，找到剛剛自動開立的沖銷傳票，確認無誤後全數點選【通過】。</td>
        <td class="chk-pages"><span class="p-tag">P.92 ~ P.94</span></td>
      </tr>
      <tr>
        <td class="chk-box">☐</td>
        <td class="chk-step">Step 3</td>
        <td class="chk-mod"><span class="mod mod-anji">安基作業</span></td>
        <td>回到安基【帳務處理】向右滑動底部橫條，確認「是否沖銷」欄位皆顯示為<strong>【是】</strong>即完成全流程 (<span class="p-tag">P.94~95</span>)。</td>
        <td class="chk-pages"><span class="p-tag">P.94 ~ P.95</span></td>
      </tr>
      <tr>
        <td class="chk-box">☐</td>
        <td class="chk-step">傳票檢視</td>
        <td class="chk-mod"><span class="mod mod-anji">安基作業</span></td>
        <td>於【帳務處理】點選個別社員「綠色鉛筆」(<span class="p-tag">P.126</span>)，可分別點選檢視：①<strong>收款傳票</strong> (<span class="p-tag">P.127~128</span>)、②<strong>墊付傳票</strong> (<span class="p-tag">P.129~130</span>)、③<strong>沖銷傳票</strong>（含代收互助基金、意外險墊款、經辦收入，<span class="p-tag">P.131~132</span>）。</td>
        <td class="chk-pages"><span class="p-tag">P.125 ~ P.132</span></td>
      </tr>
    </table>
  </div>

  <!-- ==================== PAGE 4 ==================== -->
  <div class="page-break"></div>

  <div class="sec-h2">
    <span>四、補充說明：三大付款方式詳細步驟檢核表（P.96 ~ P.124）</span>
    <span class="meta">搭配第一頁對照表使用</span>
  </div>

  <div class="phase-card">
    <div class="phase-card-header">
      <span>付款方式 A：【現金收款】詳細步驟（共 9 步，於臨櫃作業執行）</span>
      <span class="p-tag">P.98 ~ P.106</span>
    </div>
    <table class="chk-table">
      <tr>
        <td class="chk-box">☐</td>
        <td class="chk-step">Step 1~4</td>
        <td class="chk-mod"><span class="mod mod-counter">臨櫃作業</span></td>
        <td>切換到【臨櫃作業】(<span class="p-tag">P.98</span>) ➔ 點選【社員搜尋】(<span class="p-tag">P.99</span>) ➔ 輸入【社員帳號】查詢 (<span class="p-tag">P.100</span>) ➔ 找到該社員點選【選擇】(<span class="p-tag">P.101</span>)。</td>
        <td class="chk-pages"><span class="p-tag">P.98 ~ P.101</span></td>
      </tr>
      <tr>
        <td class="chk-box">☐</td>
        <td class="chk-step">Step 5~9</td>
        <td class="chk-mod"><span class="mod mod-counter">臨櫃作業</span></td>
        <td>點選【現金收款作業】(<span class="p-tag">P.102</span>)，系統自動帶出代辦互助基金應繳金額 (<span class="p-tag">P.103</span>) ➔ <strong>把其他無關項目都點選【移除】</strong>(<span class="p-tag">P.104</span>) ➔ 點選【確認收款並列印收款單】(<span class="p-tag">P.105</span>)，顯示開立成功即可列印傳票 (<span class="p-tag">P.106</span>)。</td>
        <td class="chk-pages"><span class="p-tag">P.102 ~ P.106</span></td>
      </tr>
    </table>
  </div>

  <div class="phase-card">
    <div class="phase-card-header">
      <span>付款方式 B：【備轉金】詳細步驟（共 5 步，於會計作業確認傳票）</span>
      <span class="p-tag">P.107 ~ P.111</span>
    </div>
    <table class="chk-table">
      <tr>
        <td class="chk-box">☐</td>
        <td class="chk-step">Step 1~5</td>
        <td class="chk-mod"><span class="mod mod-acc">會計作業</span></td>
        <td>於安基加保時付款方式選【備轉金】並送出 (<span class="p-tag">P.107</span>) ➔ 點擊右上角【切換】至【會計作業】(<span class="p-tag">P.108</span>) ➔ 點選左側【傳票確認作業】(<span class="p-tag">P.109</span>) ➔ 找到剛剛那張傳票，點選【通過並列印】(<span class="p-tag">P.110</span>)，顯示開立成功 (<span class="p-tag">P.111</span>)。</td>
        <td class="chk-pages"><span class="p-tag">P.107 ~ P.111</span></td>
      </tr>
    </table>
  </div>

  <div class="phase-card">
    <div class="phase-card-header">
      <span>付款方式 C：【應付代收】詳細步驟（共 13 步：會計開立轉帳傳票 ➔ 安基送出 ➔ 會計傳票確認）</span>
      <span class="p-tag">P.112 ~ P.124</span>
    </div>
    <table class="chk-table">
      <tr>
        <td class="chk-box">☐</td>
        <td class="chk-step">Step 1~4</td>
        <td class="chk-mod"><span class="mod mod-acc">會計作業</span></td>
        <td>先切換到【會計作業】(<span class="p-tag">P.112</span>) ➔ 點選【傳票管理】下的【開立傳票】（支出轉帳傳票，<span class="p-tag">P.113</span>）➔ 點選【新增傳票項目】(<span class="p-tag">P.114</span>) ➔ 輸入第一筆分錄：選擇社員、輸入社員帳號、調整會計科目（如 <code>11211 活期存款</code>）、輸入應繳金額、選<strong>【借方】</strong>按確定 (<span class="p-tag">P.115</span>)。</td>
        <td class="chk-pages"><span class="p-tag">P.112 ~ P.115</span></td>
      </tr>
      <tr>
        <td class="chk-box">☐</td>
        <td class="chk-step">Step 5~8</td>
        <td class="chk-mod"><span class="mod mod-acc">會計作業</span></td>
        <td>再次點選【新增傳票項目】(<span class="p-tag">P.116</span>) ➔ 輸入第二筆分錄：選擇對應代收互助基金科目（如 <code>21515 代收重大疾病互助基金</code> 或 <code>21514 代收社員意外互助基金</code>）、輸入相同金額、選<strong>【貸方】</strong>按確定 (<span class="p-tag">P.117</span>) ➔ 點選【送出】(<span class="p-tag">P.118</span>)，顯示開立成功 (<span class="p-tag">P.119</span>)。</td>
        <td class="chk-pages"><span class="p-tag">P.116 ~ P.119</span></td>
      </tr>
      <tr>
        <td class="chk-box">☐</td>
        <td class="chk-step">Step 9</td>
        <td class="chk-mod"><span class="mod mod-anji">安基作業</span></td>
        <td>回到【安基作業】該筆加保資料，此時【應付代收】下方的<strong>【結餘】就會顯示剛剛轉入的金額</strong>；有結餘後先點【暫存】再按【送出】(<span class="p-tag">P.120</span>)。</td>
        <td class="chk-pages"><span class="p-tag">P.120</span></td>
      </tr>
      <tr>
        <td class="chk-box">☐</td>
        <td class="chk-step">Step 10~13</td>
        <td class="chk-mod"><span class="mod mod-acc">會計作業</span></td>
        <td>再次切換到【會計作業】(<span class="p-tag">P.121</span>) ➔ 點選左側【傳票確認作業】(<span class="p-tag">P.122</span>) ➔ 找到剛剛那張傳票，點選【通過並列印】(<span class="p-tag">P.123</span>)，顯示開立成功 (<span class="p-tag">P.124</span>)。</td>
        <td class="chk-pages"><span class="p-tag">P.121 ~ P.124</span></td>
      </tr>
    </table>
  </div>

  <div class="sec-h2">
    <span>五、常見問題與防呆排錯指南（FAQ，原簡報 P.133 修正補充版）</span>
    <span class="meta">遇到畫面沒按鈕或找不到傳票時請優先查閱</span>
  </div>

  <div class="faq-box">
    <div class="faq-q">
      <span>Q1：為何我在【會計作業 ➔ 傳票確認作業】找不到傳票？</span>
      <span class="p-tag">P.133</span>
    </div>
    <div class="faq-a">
      <strong>解答：</strong>請主管切換至<strong>【審核作業】</strong>那邊檢視是否有互助基金相關傳票需要審核，<strong>主管審核通過後</strong>，【傳票確認作業】才會出現該張傳票。
    </div>
  </div>

  <div class="faq-box warn">
    <div class="faq-q">
      <span>Q2：為何在【加退保合併送件】畫面上沒有顯示【送至協會】按鈕？</span>
      <span><span class="p-tag">P.66~69</span> <span class="p-tag">P.133</span></span>
    </div>
    <div class="faq-a">
      <strong>解答：</strong><em>（註：原簡報 P.133 第二題文字誤植為第一題回答，此處依 P.66~69 系統實際流程修正）</em><br/>
      ① 請確認在【加退保合併送件】明細中是否已點選<strong>【確認名單，送主管審查】</strong>（狀態為「已送出審查」，<span class="p-tag">P.66~67</span>）。<br/>
      ② 送出審查後，請主管至<strong>【審核作業】</strong>將該筆合併送件名單（以及關聯的互助基金傳票）審核通過 (<span class="p-tag">P.68</span>)。<br/>
      ③ 主管審核完成後，重新進入該筆【加退保合併送件】，畫面上才會出現<strong>【送至協會】</strong>按鈕 (<span class="p-tag">P.69</span>)。
    </div>
  </div>

  <div class="faq-box danger">
    <div class="faq-q">
      <span>Q3：名冊已經點選【送至協會】，但事後發現有錯，怎麼辦？</span>
      <span class="p-tag">P.133</span>
    </div>
    <div class="faq-a">
      <strong>解答：</strong>一旦點選【送至協會】，系統即無法線上退回修改。在核保通過前若要變更資料，<strong>必須送紙本辦理變更（過程可能要等 1 個月）</strong>。因此送出前務必透過【預覽名冊】(<span class="p-tag">P.50</span>) 與【列印名冊】(<span class="p-tag">P.60</span>) 完整確認！
    </div>
  </div>

  <div class="faq-box warn">
    <div class="faq-q">
      <span>Q4：新加保或調整資料選擇【應付代收】時，為何畫面下方的【結餘】顯示為 0？</span>
      <span><span class="p-tag">P.24</span> <span class="p-tag">P.112~120</span></span>
    </div>
    <div class="faq-a">
      <strong>解答：</strong>代表費用尚未轉到該互助基金。請先至<strong>【會計作業 ➔ 傳票管理 ➔ 開立傳票】</strong>開立支出轉帳傳票（借：社員活期存款／貸：代收互助基金），送出後回到【安基作業】就會顯示【結餘】，此時即可先點【暫存】再按【送出】。
    </div>
  </div>

  <div class="sec-h2">
    <span>六、常用會計傳票分錄速查卡（依簡報範例整理）</span>
    <span class="meta">實際科目請依各社／基金別選用</span>
  </div>

  <table class="comp-table">
    <thead>
      <tr>
        <th style="width:24%;">傳票時機與類型</th>
        <th style="width:34%;">借方科目（Debit）</th>
        <th style="width:34%;">貸方科目（Credit）</th>
        <th style="width:8%;">對應頁碼</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>1. 應付代收前置轉帳</strong><br/>（支出轉帳傳票）</td>
        <td><code>11211 活期存款</code>（選擇社員帳號）</td>
        <td><code>21514 代收社員意外互助基金</code> 或<br/><code>21515 代收重大疾病互助基金</code></td>
        <td><span class="p-tag">P.115~117</span></td>
      </tr>
      <tr>
        <td><strong>2. 建立請款單墊付</strong><br/>（現金支出／轉帳傳票）</td>
        <td><code>11514 團體意外險墊款</code></td>
        <td><code>110122 零用金</code>（或銀行存款）</td>
        <td><span class="p-tag">P.77, 130</span></td>
      </tr>
      <tr>
        <td><strong>3. 核保通過後自動沖銷</strong><br/>（系統自動產生沖銷傳票）</td>
        <td><code>21514 代收社員意外互助基金</code></td>
        <td><code>11514 團體意外險墊款</code><br/><code>41131 團體意外險經辦收入</code></td>
        <td><span class="p-tag">P.93, 132</span></td>
      </tr>
    </tbody>
  </table>

  <div class="footer-note">
    安基作業（協會代辦互助基金）精簡版 SOP 速查手冊｜如需檢視 133 頁高解析紅框畫面，請開啟同資料夾下之 <strong>index.html</strong> 互動式網頁
  </div>

</body>
</html>
"""


def find_browser():
    candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    raise FileNotFoundError("Neither Chrome nor Edge was found.")


def main():
    browser_exe = find_browser()
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tmp:
        tmp.write(HTML_CONTENT)
        tmp_html_path = tmp.name

    try:
        cmd = [
            browser_exe,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={OUTPUT_PDF}",
            tmp_html_path,
        ]
        subprocess.run(cmd, check=True)
    finally:
        if os.path.exists(tmp_html_path):
            os.remove(tmp_html_path)

    doc = fitz.open(OUTPUT_PDF)
    print(f"Successfully generated: {OUTPUT_PDF}")
    print(f"Total A4 pages: {len(doc)}")
    doc.close()


if __name__ == "__main__":
    main()
