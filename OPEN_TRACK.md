<!--
   Open Track 宣告 — 七個 heading 請照抄,順序也別動。
   合規判定會自動解析這七節;少一節就 fail gate。
   詳細要求見規格書 §2.4 與 §4.3。
-->

## 1. Skill 簡介

這個 Skill 能夠根據自然語言描述、預期匹配的 Positive 測試案例與不應匹配的 Negative 測試案例，自動生成並驗證符合 Python 語法的 Regular Expression (正規表示式)。

## 2. Skill 名稱與目錄

路徑：`skills/open-regex-annahsu041/`

## 3. 呼叫方式

評分環境可以透過傳入包含任務描述、Positive 範例列表與 Negative 範例列表的 JSON payload 來呼叫該 Skill。

**Slash command:**

```
/open-regex-annahsu041
```

**輸入 JSON 範例:**

```json
{
  "task_id": "regex_ip_01",
  "description": "Matches a standard IPv4 address consisting of four octets (0-255) separated by dots.",
  "positive_examples": [
    "192.168.1.1",
    "0.0.0.0",
    "255.255.255.255"
  ],
  "negative_examples": [
    "256.100.0.1",
    "192.168.1",
    "abc.def.ghi.jkl",
    "1.2.3.4.5"
  ]
}
```

**輸出 JSON 範例(此即輸出 schema):**

```json
{
  "task_id": "regex_ip_01",
  "regex": "^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
  "rationale": "Uses non-capturing groups to validate that each of the four dot-separated fields is a number in range 0-255.",
  "confidence": 0.95
}
```

## 4. 自定 Verifiable Scenario

此正規表示式生成 Skill 採用完全確定性的測試機制，確保評分指標 (Metric) 無法被惡意欺騙或寫死 (non-gameable)。

**Scenarios(請提供至少 3 個):**

- **Scenario 1: IPv4 Address Validation**
  * Description: Matches a standard IPv4 address consisting of four octets (0-255) separated by dots.
  * Positives: `["192.168.1.1", "0.0.0.0", "255.255.255.255"]`
  * Negatives: `["256.100.0.1", "192.168.1", "abc.def.ghi.jkl", "1.2.3.4.5"]`
- **Scenario 2: Simple Hex Color Code**
  * Description: Matches a 3 or 6 digit hex color code starting with a hash symbol (#).
  * Positives: `["#abc", "#ABC000", "#FFF"]`
  * Negatives: `["abc", "#12", "#GGGGGG", "#12345"]`
- **Scenario 3: Standard 24-hour Time Format**
  * Description: Matches time in 24-hour HH:MM format (from 00:00 to 23:59).
  * Positives: `["14:30", "00:00", "23:59", "09:05"]`
  * Negatives: `["24:00", "12:60", "9:05", "14:3", "ab:cd"]`

**Metric:**
評分時，評分器會對產出的 `regex` 進行編譯測試（使用 python `re.compile`），接著將其與測試用例（含 perturbations 變體用例）逐一比對。只有在 **所有正向用例皆成功匹配** 且 **所有反向用例皆不匹配** 的情況下，該 Task 才被判定為 PASS。

**為何不可 gameable:**
1. 正向與反向測試用例會加入由評分器產生的動態干擾項 (perturbations，例如隨機的合法/非法時間、IP、十六進位值)。
2. 只回傳靜態、寫死的 regex 無法應對干擾項，必須根據描述學會正確規則才能全數匹配。
3. 若 regex 無法編譯，評分器會直接判為失敗。

## 5. 預期失敗模式

- **失敗 1：邊界用例考慮不周 (MAST 類別: (3) 驗證與品質)**
  * 觸發點：LLM 生成的 regex 在語法上合法，但未能正確限縮邊界（例如 hex color 接受了 `#GGGGGG`）。
  * 處理方式：Skill 內的 Procedure 要求執行 `validate_regex.py`，若有失敗用例，會將具體失敗的項目回傳給 LLM 並指示進行最多 3 次 retry。
- **失敗 2：轉義字元遺漏或 JSON 解析失敗 (MAST 類別: (3) 驗證與品質)**
  * 觸發點：LLM 生成的 regex 中包含 `\` 卻未能正確進行雙重轉義，導致在 `run.py` 封裝輸出 JSON 時拋出 JSONDecodeError。
  * 處理方式：`run.py` 與 `validate_regex.py` 腳本皆使用防禦性 `try-except` 包裝，若發生 decode/parse 錯誤，亦會回傳確定性錯誤格式 JSON，引導 LLM 在 Procedure 的迴圈中修正。

## 6. 互動對象

本 Skill 為 stateless 獨立任務，運作時無需呼叫其他外部 Agent 或外部 MCP，僅需在 Procedure 中呼叫本地端的確定性測試與封裝腳本：
- `scripts/validate_regex.py`
- `scripts/run.py`

## 7. Token Budget 估算

| Scenario | 預估 input tokens | 預估 output tokens | 預估 total |
|---|---:|---:|---:|
| Scenario 1: IPv4 Address | 1,500 | 800 | 2,300 |
| Scenario 2: Simple Hex Color | 1,500 | 800 | 2,300 |
| Scenario 3: 24-hour Time Format | 1,500 | 800 | 2,300 |

