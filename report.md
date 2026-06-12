# 期末報告 — AIASE 2026 Final Project

> 學生: Annahsu / GitHub: `annahsu041`

---

## 1. 設計決策

本專案圍繞「用確定性的外殼，包住機率性的核心（deterministic shell wrapping probabilistic core）」原則，在 Hermes Agent 上實現可自動驗證的技能。

### 1.1 Basic — Text2SQL Skill
* **Harness 設計：** 我們使用了 `scripts/validate_sql.py` 作為確定性驗證外殼。在 LLM 生成 SQL 之後，不直接返回，而是先利用內建 sqlite3 建立一個內存臨時資料庫，並將傳入的 `db_schema` 執行建表，再對生成的 SQL 執行 `EXPLAIN <sql>`。
* **設計考量：** 藉此在無實際數據的情形下快速靜態檢查「語法是否正確」以及「所用欄位/資料表是否存在」。若失敗則捕獲 sqlite3.Error 將錯誤訊息帶回給 LLM 重新規劃（限制 3 次重試）。這大大降地了拼寫錯誤與邏輯實體引用錯誤等低級失誤，將不可控的機率性核心約束在確定性規則之內。

### 1.2 Pairwise — Code Author & Bug Hunter
* **Code Author Harness 設計與考量：** 在 `scripts/selftest.py` 中，我們定義了靜態與動態結合的自測機制。一方面利用 AST 分析 `ast.Import` 與 `ast.ImportFrom` 來靜態攔截 `imports_forbidden` 違規；另一方面呼叫 `radon raw` 確定 Python 實體 S-LOC 不超過 500 行限制。動態上，則利用一組基礎邊界測試用例（如空列表 `[]`、單元素等）直接 `exec` 執行代碼來比對結果。將 sandbox 的安全限制（如禁止進程呼叫、特定庫載入）移至自測外殼（selftest harness）中先行攔截。若失敗，直接將 exit code 與測試錯誤詳情反饋給 LLM 進行自動 retry 修復，藉此保證最終輸出的程式碼 100% 能夠在 grader 沙箱中編譯並安全執行。
* **Bug Hunter Harness 設計與考量：** 在 `scripts/analyze.py` 中，我們實作了確定性邊界測量探針（Probing）。該腳本會靜態利用 AST 提取待測函數名稱與結構行號，並動態建構一套通用邊界測量電池（包括空串、None、極值與大整數），以 `exec` 在沙箱中執行，並從 traceback 中精確擷取崩潰的行號與錯誤類型。 LLM 獲得這些探針回傳的確定性錯誤信號後，能極為精準地定位 `off_by_one` 或 `edge_case` 等 bug，並可有效抑制 False Positive（誤報率），取得更好的 F1-Score。

### 1.3 Open Track — Regex Synthesis (`open-regex-annahsu041`)
* **Harness 設計：** 設計了 `scripts/validate_regex.py`，傳入候選 Regular Expression (正規表示式) 以及正向/反向測試案例。利用 `re.compile` 先行編譯檢查，再使用 `search` 來測試是否匹配 positive_examples 且不匹配 negative_examples。
* **設計考量：** 正規表示式在實踐中極易因邊界不當（如 unanchored regex）造成多餘匹配或誤判。在 harness 中將每一個測試結果詳細分類，哪一筆 positive 漏配、哪一筆 negative 被誤配，明確回傳給 LLM 使其能對症下藥修改 Regex。這種防禦性自測 retry 迴圈極大提升了生成正規表示式的跨模型穩健性。

---

## 2. 實際遭遇之失敗與分析

### 失敗 1 — Windows 環境下的控制台 CP950 編譯錯誤
- 觸發場景：在本機 Windows Terminal 執行 `python verify_repo.py` 或 `python run_dev.py` 時系統崩潰。
- log 片段：
  ```
  Traceback (most recent call last):
    File "C:\Users\User\OneDrive\Desktop\final-project-annahsu041\verify_repo.py", line 295, in <module>
      sys.exit(main())
    File "C:\Users\User\OneDrive\Desktop\final-project-annahsu041\verify_repo.py", line 289, in main
      print(f"   \u2717 {c.name}: {c.detail}")
  UnicodeEncodeError: 'cp950' codec can't encode character '\u2717' in position 3: illegal multibyte sequence
  ```
- 成因分析：腳本中使用 Unicode 符號 `✓` (\u2713) 與 `✗` (\u2717) 來列印測試結果。在 Windows 控制台預設為 CP950 語系環境下，該字元集無法識別此 Unicode 符號，因而丟出不可恢復的轉碼異常。
- 修正方式：在 `verify_repo.py` 與 `run_dev.py` 中，將所有的特殊圖標 `✓` 與 `✗` 全數替換為 ASCII 標準標籤 `[PASS]` 與 `[FAIL]`。
- MAST 分類(選用): (3) 驗證與品質

### 失敗 2 — 自動生成的 Spec 檔案觸發 verify 絕對路徑警告
- 觸發場景：執行 `verify_repo.py` 時，出現 no-absolute-paths 檢查失敗。
- log 片段：
  ```
  [FAIL] no-absolute-paths: found 2 hit(s); first: TAICA2026_FinalProject_Spec.md: C:\\Users\\...
  ```
- 成因分析：為了保留網頁的完整作業說明，我們造訪網頁轉換產生的 `TAICA2026_FinalProject_Spec.md` 包含多個 `C:\Users\...` 範例絕對路徑，從而觸發了 `verify_repo.py` 嚴格的絕對路徑掃描過濾。
- 修正方式：在 `verify_repo.py` 中，將 `"TAICA2026_FinalProject_Spec.md"` 加入 `no-absolute-paths` 的排除檔案清單（與 `README.md` 和 `verify_repo.py` 相同），使其跳過對該參考文件的路徑掃描。
- MAST 分類(選用): (1) 規格與角色

### 失敗 3 — 殘留的 verify_report.json 遞迴觸發路徑警告
- 觸發場景：上一次驗證失敗產生的 `verify_report.json` 文件導致下一次驗證同樣失敗。
- log 片段：
  ```
  [FAIL] no-absolute-paths: found 1 hit(s); first: verify_report.json: C:\\Users\\...
  ```
- 成因分析：`verify_repo.py` 在執行後會將詳細的錯誤報告（包含上一次失敗的絕對路徑訊息）寫入根目錄的 `verify_report.json`。在下一次重新執行檢驗時，該 json 文件同樣會被遍歷，導致其內部記錄的絕對路徑再度被掃描判定為違規，形成遞迴誤判。
- 修正方式：將 `"verify_report.json"` 同樣加入到 `verify_repo.py` 的 absolute-path 檢查忽略清單中。
- MAST 分類(選用): (3) 驗證與品質

---

## 3. 改進方向

1. **整合 pytest 自動化驗證：** 目前 `run_dev.py` 使用了子進程呼叫 CLI 的方式自測。未來如果能在 `tests/` 中封裝直接載入 Skill 模組的單元測試，將極大提速測試的反覆運算。
2. **對對手程式碼提供動態 Fuzz 測試：** 在 Bug Hunter 與 Open Track 的自測中，如果能利用 Fuzzing 庫（例如 `hypothesis`）為函數生成隨機極端邊界資料，將能大幅提升代碼自測與 Bug 定位的召回率。
3. **異步多模型投票 (Ensemble Check)：** 開發期可利用 `LiteLLM` 同時對 Gemma 與 Gemini 獲取結果，並在 `scripts/` 中加入一個簡單的語意比對模組，只有在多數模型達成共識時才確認輸出，減小單一模型隨機性錯誤。

---

## 5. 引用說明

* **來源：** NousResearch/hermes-agent 官方 Repository (https://github.com/NousResearch/hermes-agent)
  * **使用範圍：** 參考了其 `SKILL.md` 規範、Metadata 設計架構與 Skill 的 procedures 呼叫語法。
  * **差異：** 我們的版本移除了所有外部 MCP server 依賴，並藉由 python 確定性腳本 `validate_sql.py` 與 `validate_regex.py` 將執行與結果比對全數限制在 Agent 平台的內建 sandbox/terminal 環境內，最大程度確保無外網環境下的可重現性。

