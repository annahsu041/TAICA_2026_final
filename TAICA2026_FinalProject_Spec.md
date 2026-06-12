# 🏛️ 期末專案：在 Hermes Agent 上打造可驗證的 Skill
*課程：AIASE 2026 · 莊坤達 · NCKU CSIE　·　文件日期 2026-05-29*

> **課程期末大型作業｜Verifiable Skills & Multi-Agent Engineering on Hermes Agent**
> 
> 本專案為延續 HW1–HW4 的一個較大型作業，請以「規模較大的作業」視之，依規格逐步完成。
> 
> 繳交方式：上傳至 GitHub Classroom

> [!WARNING]
> **公告**
> **請特別注意：本次期末成果將對外公布。** 完成後，課程會將整體成果透過 **TAICA（臺灣人工智慧卓越中心聯盟課程平台）對外宣布**。這代表你的努力不只是一份課堂作業，而會成為一個公開、可被看見的工程成果 —— 也因此，**程式碼的誠信、引用規範與可重現性格外重要**（詳見 §六）。

---

## Deadline

所有 deadline 皆以 **Asia/Taipei（UTC+8）** 時間為準。

| 階段 | 截止時間 |
| --- | --- |
| **Team-of-Two proposal（如要組 2 人團隊）** | 2026/6/2 23:59 |
| **最終繳交（skills + report）** | **2026/6/16 23:59** |
| **Demo Day（於課程 Hermes Agent 評分）** | 2026/6/17 上課時間 |

> [!NOTE]
> **重點**
> **不允許遲交。** 2026/6/16 23:59:00 Asia/Taipei 之後 push 到 GitHub 的 commit 完全不會被納入評分。課程將於 deadline 一過把全部 repo clone 至地端，6/17 於課程的 Hermes Agent 上評分，無補交、無延長。

### 評分版本定義

評分版本以 deadline 當下 GitHub 上可取得的 repo 狀態為準：

1. 以 **2026/6/16 23:59:00 Asia/Taipei** 時，GitHub 上 **default branch** 可取得的最新 commit 為準。
2. `commit author date` / `committer date` 不作為是否準時的依據。
3. deadline 後才 push 到 GitHub 的 commit，即使 commit 本身時間早於 deadline，也不納入評分。
4. 若學生使用非 default branch，必須在 deadline 前 merge 到 default branch；評分器不會自動搜尋其他 branch。
5. 課程 clone 後會記錄 repo URL、default branch、commit SHA、clone timestamp 作為 audit log。

---

## 期末專案目標

> **Verifiable Skill Engineering on a Real Agent** — 把整學期的核心原則「**用確定性的外殼，包住機率性的核心**（deterministic shell wrapping probabilistic core）」，落實到一個**真實、業界廣泛使用的 agent 平台**上：你要為 [NousResearch 的 **Hermes Agent**](https://github.com/NousResearch/hermes-agent) 開發 Skill，使其在「不可預測的 LLM 核心」之上，仍能產生**可被自動驗證（verifiable）**的結果。

本期末專案的核心學習目標：

- 為真實 agent 平台撰寫符合 **agentskills.io 開放標準** 的 Skill（`SKILL.md` + `scripts/`），理解 skill 如何被 agent 載入、觸發、執行。
- 設計**不可 gameable 的 verifiability metric**，把 harness engineering 與 verifiability mindset 落實到 skill 的 `scripts/` 與 `## Verification` 區塊。
- 區分系統中的 **deterministic 層（你寫的 skill）與 probabilistic 層（Hermes 的 LLM agent loop）**，理解可靠的 agentic 系統如何被工程化。
- 親身體驗 multi-agent 協作的**失敗模式**，並於報告中以執行紀錄（log）證據進行結構化分析（可選用 MAST taxonomy 作為分類詞彙，見 §4.4）。

> [!WARNING]
> **注意**
> **本專案的評分依據是「skill 在 Hermes Agent 上能否被自動驗證地執行」，而非「概念的視覺新穎度」。** 一個結構簡單、但裝進 Hermes 後能穩定通過所有 verifiable scenario 的 skill，視為完成；一個看似複雜、但裝不起來或輸出無法被驗證的 skill，視為未完成。

> [!TIP]
> **提示**
> **為什麼選 Hermes Agent？** 因為它是真實、開源（MIT）、社群活躍的 agent 平台 —— 你做出來的不是一個只能在課程虛構環境跑的玩具，而是任何裝了 Hermes 的人都能 `hermes skills install` 直接使用的通用 skill。這也是本專案刻意更接近真實世界的地方。

---

## 分組規定

- **原則上一人一組（單人專案）。**
- 若需**兩人一組**，兩位同學須於 **2026/6/2 23:59 Asia/Taipei** 前提交 Team-of-Two proposal，並經課程核准；未核准者視為單人組。
- 兩人組使用單一 repo 繳交，兩位成員原則上獲得相同分數。
- Proposal 必須列出兩位成員分工，且 `report.md` 必須回填實際分工。

### 兩人組最低要求

兩人組不應以單人規模之工作量繳交。最低要求如下：

1. **Basic Track**：仍須完成同一份 Basic skill。
2. **Pairwise Track**：建議兩個角色皆實作，或實作一個顯著強化版本；若只實作一個角色，須在 report 中說明另一位成員的實質貢獻。
3. **Open Track**：須包含至少兩個可獨立驗證的 scenario，或一個明顯高於單人規模的 multi-skill / multi-agent 設計。

若最終成果經 rubric 判定未達兩人組最低要求，總分將乘上 **0.90 至 0.99** 的 pair-size adjustment factor。factor 由課程依 proposal、repo commit、report 分工與實際成果綜合判定。

---

## 評分與爭議處理共通原則

本專案參與人數多，為避免後續執行爭議，所有評分與申覆皆依以下原則處理：

1. **Repo 內容優先**：評分只依 deadline 前 default branch 中的檔案、程式、設定與文件執行。deadline 後的口頭補充、訊息說明或額外檔案不納入評分。
2. **機器可讀優先**：凡本規格要求固定檔名、JSON 欄位、section heading、skill name 或 command format 者，皆以機器可解析結果為準。
3. **Log 為準**：課程會保存安裝、執行、JSON 擷取、hidden test、Open Track judge 與 Pairwise 配對 log。分數爭議以該 log 與評分程式輸出為主要依據。
4. **固定環境**：評分以 starter repo / grading image 指定的 Hermes、Python、dependency 與模型 gateway 設定為準。學生本機可執行不代表評分環境必定可執行。
5. **No hidden assumptions**：若 Open Track 或 skill 需要特定呼叫方式、資料、依賴、互動對象或 evaluator，必須在指定檔案中明確寫出；未寫出者視為不存在。
6. **安全與可重現性優先**：任何需要外部服務、個人 secret、非課程授權 API、網路狀態或本機絕對路徑才能成功的設計，評分時不保證可用；若因此失敗，該部分不得分。
7. **不得以事後意圖取代文件內容**：Open Track、Pairwise role、skill path、metric、schema 等若在 repo 中未明確寫出，不得於 deadline 後以「原本想表達的是……」補充。

---

## 一、背景說明

### 1.1 為何設計本專案

主軸是「deterministic shell wrapping probabilistic core」：從 harness engineering、spec-driven development、到 context engineering，每個課程主題都在示範此原則的不同切面。期末專案是此原則的最終測驗 —— 而且是在**真實平台**上測。

過去的作業多半是 standalone 的小程式。本專案不同：你寫的東西要能**裝進一個真實、別人也在用的 agent（Hermes Agent）**並穩定運作。這必須思考一個真實世界的核心問題：當底層 agent 的 LLM 行為不可預測時，你寫的 skill 如何仍能產生**可被客觀驗證**的結果？答案就是 harness engineering —— 把確定性的驗證、retry、結構化輸出包在 skill 的 `scripts/` 裡，讓 LLM 的機率性被你的確定性外殼框住。

### 1.2 Hermes Agent 與你的 Skill 的關係

**Hermes Agent** 是 NousResearch 開源的 agent 平台。它本身是一個 LLM 驅動的 agent loop（會推理、呼叫工具、管理記憶）—— 這是系統中**機率性（probabilistic）**的部分。你**不修改 Hermes 本身**，而是為它撰寫 **Skill**：一個 `SKILL.md` 套件，告訴 Hermes「何時、如何」完成某個任務，並附上 `scripts/` 中的確定性 helper 程式。Skill 就是系統中**確定性（deterministic）**的外殼。

```
graph LR
  G["課程評分環境<br/>hermes chat -q 餵入 hidden 任務"] --> H["Hermes Agent<br/>LLM agent loop<br/>（probabilistic core）"]
  H -->|"載入 /your-skill"| S["你的 Skill<br/>SKILL.md + scripts/<br/>（deterministic shell）"]
  S -->|"呼叫"| SC["scripts/ harness<br/>驗證 · retry · 產生結構化輸出"]
  SC --> O["結構化輸出（JSON）"]
  O --> E["評分：對 hidden set 自動比對"]

  style H fill:#EDE5F2,stroke:#6B4F8E,color:#2A2A2A
  style S fill:#EAF1EA,stroke:#2E5E3E,color:#2A2A2A
  style SC fill:#EAF1EA,stroke:#2E5E3E,color:#2A2A2A
  style O fill:#F5F5F6,stroke:#A6A9AB,color:#555559
  style E fill:#F5F5F6,stroke:#A6A9AB,color:#555559
```
圖 1 — 你的 Skill（deterministic shell）插進 Hermes Agent（probabilistic core）

*圖 1 — 你的 Skill（deterministic shell）插進 Hermes Agent（probabilistic core），評分環境以 `hermes chat -q` 驅動並比對結構化輸出*

課程概念與 Hermes Agent 真實機制的對應：

| 課程概念 | 在 Hermes Agent 上的對應 |
| --- | --- |
| Probabilistic core | Hermes 的 LLM agent loop（你不改它） |
| Deterministic shell / harness | 你寫的 Skill：`SKILL.md` 的 Procedure/Verification + `scripts/` 的 helper 程式 |
| Verifiability mindset | `SKILL.md` 的 `## Verification` 區塊 + `scripts/` 產生的結構化、可比對輸出 |
| Skill vs. Sub-Agent | 預設用 Skill；確有多步自主推理需求才用 Hermes 的 subagent（Open Track 才考慮） |

### 1.3 Skill 規格（agentskills.io 標準）

每個交付的 skill 都是一個資料夾，至少包含一份 `SKILL.md`，並可附 `scripts/`、`references/`、`templates/`。這是 Hermes Agent 原生、且符合 [agentskills.io](https://agentskills.io) 開放標準的格式。

#### Skill 命名規則

為利全班自動安裝與評分，所有 skill folder name 與 `SKILL.md` frontmatter 中的 `name` 必須一致，且必須包含 `annahsu041`。本規格全篇以 `annahsu041` 作為唯一識別碼，不使用學號作為唯一識別碼。

建議格式：

- Basic Track：`text2sql-annahsu041`
- Pairwise Code Author：`code-author-annahsu041`
- Pairwise Bug Hunter：`bug-hunter-annahsu041`
- Open Track：`open-<short-name>-annahsu041`

`annahsu041` 以 GitHub Classroom roster mapping 為準。

#### 目錄結構範例

```text
skills/
└── text2sql-annahsu041/
    ├── SKILL.md               # 主指令（必要）
    ├── scripts/               # 可被 skill 呼叫的確定性 helper（你的 harness）
    │   ├── run.py             # 入口：產生結構化輸出
    │   └── validate_sql.py    # 例：SQL 語法驗證器
    └── references/            # 選用：補充說明
```

#### `SKILL.md` 格式

`SKILL.md` 應包含 frontmatter + 內文，皆為 Hermes 原生欄位。例如：

```markdown
---
name: text2sql-annahsu041
description: Convert a natural-language question + SQLite schema into a verified SQL query.
version: 1.0.0
metadata:
  hermes:
    tags: [sql, text2sql, data]
    category: data
---

# Text2SQL Skill

## When to Use
當收到「自然語言問題 + SQLite schema」並要求產出 SQL 時觸發。

## Procedure
1. 解析 schema，理解表與關聯。
2. 產生 SQL。
3. 呼叫 `scripts/validate_sql.py` 驗證語法與欄位是否存在；不過則帶錯誤訊息重試（至多 N 次）。
4. 呼叫 `scripts/run.py`，以下方「輸出契約」規定的結構化格式輸出最終結果。

## Pitfalls
- 多對多關聯未去重 → 結果集中多出重複列。
- 引用 schema 不存在的欄位。

## Verification
最終輸出必須是合法、可在該 schema 上執行的 SQL，且符合輸出契約之 JSON 結構。
```

### 1.4 共通輸出契約（所有 Track 必須遵守）

Skill 的**最後一個動作**必須輸出**單一一段 fenced JSON 區塊**，作為該任務的可驗證結果。評分器只會讀取 `hermes chat --toolsets skills -q` 的 stdout，並擷取其中**最後一段**以 ````json` 開頭、````` 結尾的 fenced code block。

共通規則如下：

1. fenced code block 內容必須是合法 JSON，且 top-level 必須是 object，不可為 array、string 或多個 JSON object。
2. 不允許 JSON comments、trailing comma、`NaN`、`Infinity`。
3. 必填欄位不得缺漏；除非該 Track 明確允許，否則 extra fields 會被忽略，不作為加分依據。
4. 若輸入包含 `task_id`，輸出的 `task_id` 必須與輸入完全相同。
5. `confidence` 若存在，必須是 `0.0` 到 `1.0` 之間的 number。
6. fenced JSON 區塊後不得再輸出其他 fenced JSON 區塊；若有多個 fenced JSON，評分器只採最後一個。
7. 若無法產生有效答案，也必須輸出符合契約的 JSON，不得只輸出自然語言道歉、錯誤說明或 traceback。
8. 評分器不會從自然語言段落、Markdown 表格、XML、YAML 或非最後 fenced JSON 區塊中推測答案。

> [!TIP]
> **提示**
> **為什麼用「scripts/ 產生結構化輸出」這個 pattern？** 因為 NL→SQL 這類任務的推理本質是機率性的（由 Hermes 的 LLM 完成），但「輸出格式合不合法、能不能被機器比對」必須是確定性的。把格式檢查、語法驗證、retry、最終 JSON 封裝都放進 `scripts/`，就是把確定性外殼套在機率性核心外面 —— 這正是本課程的 harness engineering。

#### Basic Track JSON schema

```text
Required fields:
- task_id: string, must equal input task_id
- sql: string, exactly one SQLite read-only query
- rationale: string
- confidence: number, 0.0 <= confidence <= 1.0

Extra fields:
- Allowed but ignored.
```

#### Pairwise — Code Author JSON schema

```text
Required fields:
- task_id: string, must equal input task_id
- code: string, Python source code
- loc: integer, source lines of code reported by the skill
- self_test_results: object, must include passed and failed counts
- rationale: string
- confidence: number, 0.0 <= confidence <= 1.0

Extra fields:
- Allowed but ignored.
```

#### Pairwise — Bug Hunter JSON schema

```text
Required fields:
- task_id: string, must equal input task_id
- verdict: string enum, one of ["buggy", "clean"]
- bugs: array of bug objects; must be [] when verdict = "clean"
- confidence: number, 0.0 <= confidence <= 1.0

Each bug object required fields:
- line_start: integer, 1-indexed
- line_end: integer, 1-indexed, must be >= line_start
- severity: string enum, one of ["critical", "high", "medium", "low"]
- type: string enum, see §2.3
- description: string
- suggested_fix: string

Extra fields:
- Allowed but ignored.
```

#### Open Track JSON schema

Open Track 的輸出 schema 由學生在 `OPEN_TRACK.md` 的「## 3. 呼叫方式」與「## 4. 自定 Verifiable Scenario」中自行定義，但仍須符合共通輸出契約。若 scenario 輸入包含 `task_id`，輸出也必須包含相同 `task_id`。若未明確定義輸出 schema，Open Track 合規判定可能失敗。

### 1.5 確定性 code 放 `scripts/`，不要用 MCP（重要觀念澄清）

課程只教過 MCP，部分同學會誤以為「skill 要呼叫本地的確定性 Python（例如檢查 code 能否 compile、跑單元測試、用 SQLite 驗 SQL 語法）就一定得透過 MCP」。**這是錯的。本專案請一律把確定性 code 放在 skill 的 `scripts/` 下，不要用 MCP。**

**為什麼不用 MCP？** 先釐清兩者的角色：

- **MCP（Model Context Protocol）** 是用來把 agent 連到 **skill 外部、獨立運行的跨行程服務**（你另外架的 server、別人的 API、跨機器的工具）。它的存在是為了「連到一個本來就獨立於 agent 的外部系統」。
- **Hermes 的 `scripts/`** 是 skill **自帶**的 helper 程式。Hermes Agent 內建 `terminal` / `execute_code` 等工具 —— 你只要在 `SKILL.md` 的 Procedure 用自然語言指示 agent「執行 `scripts/xxx.py`」，Hermes 就會用這些內建工具去跑它、把 stdout 與 exit code 讀回來。**呼叫本地確定性 code 完全不需要 MCP，這是 skill 原生、最直接的做法。**

換句話說：**「這段確定性邏輯只服務我這個 skill」→ 放 `scripts/`；「這是多個 agent／多台機器都要連的共用外部服務」→ 才考慮 MCP。** 本專案所有的驗證邏輯（compile 檢查、test runner、SQL validator、SLOC 計算）都屬於前者，請一律放 `scripts/`。用 MCP 不但是殺雞用牛刀，還會讓評分環境被迫額外起 MCP server，徒增失敗點。

**範例**：驗證一段 code 能否 compile —— 純確定性、無 LLM、無網路，放 `scripts/`：

```python
# scripts/check_compile.py
import sys, py_compile, json

target = sys.argv[1]
try:
    py_compile.compile(target, doraise=True)
    print(json.dumps({"compile_ok": True, "error": ""}))
except py_compile.PyCompileError as e:
    print(json.dumps({"compile_ok": False, "error": str(e)}))
```

`SKILL.md` 的 Procedure 只要寫「執行 `scripts/check_compile.py <file>`，讀回 `compile_ok`，失敗則帶錯誤訊息重試」，Hermes 就會用內建 terminal 工具跑它。

> [!WARNING]
> **注意**
> **本專案禁止以 MCP 作為呼叫本地確定性 code 的手段。** 評分環境只會安裝你的 skill 並以內建工具執行 `scripts/`，不會為任何學生啟動外部 MCP server。若你的 skill 依賴外部 MCP 才能運作，評分時將無法執行、該部分無法得分。

### 1.6 依賴、路徑與網路政策

#### Python 依賴安裝規則

- 若 skill 目錄下存在 `scripts/requirements.txt`，評分器會在安裝該 skill 後執行：

`bash
  python -m pip install -r scripts/requirements.txt`

- `requirements.txt` 應 pin 版本，例如 `radon==6.0.1`。
- 不允許需要系統層級 `apt` / `brew` 安裝、GPU、Docker daemon、背景服務或互動式安裝的依賴。
- 若 dependency installation 失敗，該 skill 視為安裝失敗。
- 評分 runtime 不保證可連外網。若課程提供 wheel cache，僅 cache 內套件保證可用；允許套件清單以 starter repo 為準。

#### 路徑規則

- 一律用相對 skill 目錄的路徑呼叫 `scripts/`。
- 不得 hardcode 自己機器的絕對路徑，例如 `/Users/...`、`C:\Users\...`、`/home/<name>/...`。
- 評分器不保證 repo 位於與學生本機相同的路徑。

#### Runtime network policy

- 評分時，學生 skill 不得依賴外部網路服務。
- 唯一允許的 LLM 存取路徑為課程設定的 LiteLLM Gateway。
- Open Track 若需要資料，必須將資料放在 repo 內、由評分輸入提供，或使用 starter repo 明確提供的 reference data。
- 任何依賴個人 API key、個人 server、雲端資料庫、Google Drive、Notion、GitHub private resource 等外部狀態的設計，評分時不保證可用；若因此失敗，該部分不得分。

### 1.7 LLM 模型政策（重要）

本專案所使用之 LLM，**由課程統一決定，一律透過 LiteLLM Gateway 提供，學生不得自行指定外部模型供應商**。**所有 LLM API 存取（含 token / 額度）將由課程後續統一提供**，學生不需自備任何 API key。設定方式：以 `hermes model` / `hermes config` 把 Hermes 的 provider 指向課程的 LiteLLM Gateway（OpenAI-compatible endpoint）—— 精確設定值會放在 starter repo（見 §5.1）。

#### 正式計分模型池

正式分數只會來自以下模型池：

- `gemma4`
- `gemini-2.5-flash`

評分當天課程會從正式計分模型池中選定一個模型，全班使用同一模型、同一 Hermes 版本、同一評分流程。實際用哪一顆模型於評分前不公布。

#### Held-out 機制

借用 ML 中 held-out set 的概念 —— 評分當下實際讓 Hermes 用哪顆模型，事前刻意保留、不對外公布，學生無法事先得知、亦不得賭定特定模型。此舉是為了量測你的 skill / harness 的**跨模型泛化能力**，而非對特定模型的最佳化。

> [!WARNING]
> **注意**
> **skill 必須 model-agnostic。** 因評分模型為 held-out，如你依賴特定模型 default 行為格式（例如假設模型必回純 JSON）、特定 prompt 記憶之 skill，將在模型改變時失效。本專案要求的是**跨模型穩健**的工程：把語法驗證、retry-on-parse-fail、防禦性 parsing、結構化輸出封裝放進 `scripts/`，正是為了讓「底層是哪顆模型都無所謂」。此設計亦對應真實 production —— 模型會因升級、降級、成本而被抽換，綁死單一模型之 skill 十分脆弱。

#### Optional robustness run 與 ⭐ 標註

課程可能額外以 `claude-haiku-4-5` 執行部分或全部 scenarios，作為跨模型穩健性展示。此 optional robustness run **不影響 100 分總分**。若 skill 在 optional run 中亦符合輸出契約並達到課程指定門檻，成果展示時會標註 ⭐。

#### 可重現性說明

評分環境會固定模型、gateway 設定、Hermes 版本、評分程式版本、dependency 版本與輸入順序，並保存完整執行 log，以提高可重現性。LLM 本身仍可能存在非完全 deterministic 的行為，因此正式分數以課程保存之當次評分 log 為準。

---

## 二、作業內容

本專案有三個 Track，**皆為必做**：Basic、Pairwise、Open Track。每個 Track 的交付物都是一個（或一組）**可裝進 Hermes Agent 的 Skill**。其中 **Open Track 佔比最高（40%）**，因為 Basic / Pairwise 的題目是所有同學共同的固定題，作品的**差異化與個人工程能力主要靠 Open Track 展現** —— 一個用心設計、能跑、可驗證的 Open Track，是這次期末專案分數的關鍵。

### 2.1 Track 結構

| Track | % | 必做 | 評分性質 |
| --- | --- | --- | --- |
| **Basic**（單一 verifiable skill，固定題） | 30 | ✅ 必做 | 100% 自動評分 |
| **Pairwise**（雙 skill 協作，固定題） | 20 | ✅ 必做；二擇一角色 | 100% 自動評分 |
| **Open Track**（自選題目，自定 verifiable scenario） | 40 | ✅ 必做 | 合規 gate（pass/fail）+ scenario 70% + 互動 log 30% |
| **報告 + Demo Day** | 10 | ✅ 必繳 | 設計決策與失敗分析 |

> [!TIP]
> **提示**
> **為什麼 Open Track 佔 40%？** Basic 與 Pairwise 是固定題（NL→SQL、Code Author / Bug Hunter），所有同學的題目與評分 metric 都一樣 —— 它們是讓你熟悉 Hermes skill 機制、學會輸出契約與 harness engineering 的暖身與基本功。**真正展現你個人工程判斷、能讓你的作品與他人不同的，是 Open Track。** 因此它的權重最高，也最值得投入心力。

### 2.2 Basic Track — Text2SQL Skill

**任務定義**：你的 skill 須讓 Hermes Agent 在收到「自然語言問題 + SQLite schema (DDL)」後，產出一段 SQL，使其在該資料庫上執行的結果等於 ground truth 答案，並以輸出契約的 JSON 格式回傳。

**輸入**（評分環境以 `hermes chat -q` 餵入，內容形如）：

```json
{
  "task_id": "task_nl2sql_017",
  "question": "List the names of all students who scored above 90 in any course taught by professor 'Wang' in 2025.",
  "db_schema": "CREATE TABLE Students (sid INT PRIMARY KEY, name TEXT, dept TEXT);\nCREATE TABLE Courses (cid INT PRIMARY KEY, title TEXT, professor TEXT, year INT);\nCREATE TABLE Enrollments (sid INT, cid INT, score INT, PRIMARY KEY(sid, cid));",
  "dialect": "sqlite"
}
```

**輸出契約**（skill 最後須輸出此 JSON 區塊）：

```json
{
  "task_id": "task_nl2sql_017",
  "sql": "SELECT DISTINCT s.name FROM Students s JOIN Enrollments e ON s.sid = e.sid JOIN Courses c ON e.cid = c.cid WHERE c.professor = 'Wang' AND c.year = 2025 AND e.score > 90;",
  "rationale": "Join three tables; filter professor/year/score; DISTINCT to dedupe.",
  "confidence": 0.82
}
```

#### Basic Track SQL 規則

- `sql` 必須是 SQLite read-only query。
- 允許 `SELECT`、JOIN、subquery、aggregation、`ORDER BY`、`LIMIT`、`UNION` / `UNION ALL` 等範圍內語法。
- 禁止 DDL / DML，例如 `CREATE`、`DROP`、`ALTER`、`INSERT`、`UPDATE`、`DELETE`。
- 若輸出多個 SQL statement，評分器可視為輸出契約違規。
- 評分比對的是 row tuple 值；除非題目另有明定，評分器不比較 column name / alias。

#### 任務範圍（Difficulty Envelope）

為使任務「可驗證」且難度公平、有界，hidden set 與 dev set 共享以下難度範圍。**dev set 已涵蓋所有會考的 SQL 特性類型，且附帶答案供本地自測**，其難度分布與 hidden set 一致 —— 請以 dev set 校準你 skill 的強度。

| 維度 | 範圍 |
| --- | --- |
| Schema 規模 | 每題 ≤ 5 張表，單表欄位 ≤ 12 |
| JOIN | 多表 JOIN（2–3 表），含 `INNER` / `LEFT JOIN` |
| Subquery / Nested | **允許巢狀子查詢，但巢狀深度 ≤ 2**（含相關子查詢 correlated subquery） |
| 聚合與分組 | 含 `GROUP BY` / `HAVING` / `COUNT` / `SUM` / `AVG` / `MAX` / `MIN` |
| 排序與限制 | 含 `ORDER BY`、`LIMIT` |
| 集合運算 | 含 `UNION` / `UNION ALL` |
| **不會出現（明確排除）** | window function、CTE（`WITH`）、遞迴查詢、DDL/DML（僅查詢，不改資料）、跨方言語法（一律 SQLite） |

> [!TIP]
> **提示**
> **為什麼要先界定範圍**：「verifiable」不只是「結果可比對」，也包含**難度有界、公平、可預期**。知道題目最難到 nested depth ≤ 2、不會冒出 window function，你才能合理判斷 skill 的 harness 要做到多強、token 成本大概多少。

**起點與 harness 方向**：最小可行的 skill 就是一份 `SKILL.md`（教 Hermes 產 SQL）+ 一支 `scripts/run.py`（封裝結構化輸出）。可往這些方向強化 harness（皆為 harness engineering 之應用）：在 `scripts/` 內以 SQLite `EXPLAIN` / prepare 驗證語法、檢查欄位是否存在、parse 失敗帶錯誤訊息重試、schema-grounded prompting、few-shot exemplars。

> [!TIP]
> **提示**
> **harness 手段請盡量發揮，但「正確答案」不會提供給你。** 你可以自由設計各種 LLM 提示策略、或在 `scripts/` 寫 Python 來輔助 —— 例如本地以 SQLite 對 schema 做 `EXPLAIN` / prepare 確認 SQL 合法、檢查有沒有引用到不存在的欄位、parse 失敗就帶錯誤訊息重試。這些都是 deterministic harness 的典型應用，鼓勵大膽嘗試。唯一要先讓你知道的是：**我們不會提供題目的正確答案（ground truth 只存在於評分環境）**。也就是說，你可以驗「這段 SQL 合不合法、跑不跑得動」，但「執行結果到底對不對」最終只由評分環境在 hidden DB 上裁定。

#### 完整範例：一個 scenario 從頭到尾

以下示範 `task_nl2sql_017` 在 Hermes Agent 上的完整流程。

**① 評分環境驅動 Hermes**（非互動式）：

```bash
hermes chat --toolsets skills -q '/text2sql-annahsu041 {"task_id":"task_nl2sql_017","question":"List the names ...","db_schema":"CREATE TABLE Students ...","dialect":"sqlite"}'
```

**② Hermes 載入你的 skill**，依 `SKILL.md` 的 Procedure 產生 SQL，並呼叫 `scripts/validate_sql.py` 做本地語法檢查：

```python
# scripts/validate_sql.py — 你寫的確定性 harness（節錄）
import sqlite3

def syntax_ok(sql: str, schema_ddl: str) -> tuple[bool, str]:
    con = sqlite3.connect(":memory:")
    try:
        con.executescript(schema_ddl)   # 建空表（無資料）
        con.execute(f"EXPLAIN {sql}")  # 只解析，不需要資料
        return True, ""
    except sqlite3.Error as e:
        return False, str(e)            # 帶錯誤訊息回去讓 LLM 重試
    finally:
        con.close()
```

> 這支 harness 能驗「SQL 合不合法、有沒有引用不存在的欄位」，但**驗不了「結果對不對」**（手上沒有資料、沒有答案）。語法過了才輸出，可大幅降低低級錯誤。

**③ skill 最後輸出結構化結果**（評分環境擷取此 JSON）：

```json
{
  "task_id": "task_nl2sql_017",
  "sql": "SELECT DISTINCT s.name FROM Students s JOIN Enrollments e ON s.sid = e.sid JOIN Courses c ON e.cid = c.cid WHERE c.professor = 'Wang' AND c.year = 2025 AND e.score > 90;",
  "rationale": "...",
  "confidence": 0.82
}
```

**④ 評分環境在 hidden DB 上執行、與 ground truth 比對**：

```text
你的 SQL 執行結果        ground truth 結果
-------------------     -------------------
[Alice, Bob, Chen]  ==  [Bob, Alice, Chen]   → bag equality ✓（順序不計）→ 此題 PASS
```

**⑤ 一個會 fail 的對照**（漏掉 `DISTINCT`）：

```text
你的 SQL 執行結果              ground truth 結果
-------------------------     -------------------
[Alice, Bob, Bob, Chen]   !=  [Alice, Bob, Chen]   → 重複列次數不一致 → 此題 FAIL
```

> [!TIP]
> **提示**
> **教學點**：語法正確、`EXPLAIN` 也過，但**結果錯了**。這說明 self-test 擋得住語法錯、擋不住語意錯。要降低這類錯誤，harness 能做 schema grounding、few-shot 等，但最終「對不對」仍由評分環境在 hidden DB 上裁定。

### 2.3 Pairwise Track — Code Author Skill + Bug Hunter Skill

本 Track 由**兩個角色**構成，每位學生在以下二者中**擇一實作**：

- **Code Author**
- **Bug Hunter**

未選擇的角色不需提交，也不會因未提交而扣分。評分時，課程的 Hermes Agent 會把你的 skill 與另一位同學或 staff reference 的對向 skill 自動配對。你無法選擇配對對象。

#### Pairwise role 宣告

每位學生必須在 repo 根目錄提供 `PAIRWISE_ROLE.md`，內容如下：

```markdown
role: code-author
skill_path: skills/code-author-annahsu041/
```

或：

```markdown
role: bug-hunter
skill_path: skills/bug-hunter-annahsu041/
```

規則：

1. `role` 只能是 `code-author` 或 `bug-hunter`。
2. `skill_path` 必須指向實際存在的 skill 資料夾。
3. 評分器只依 `PAIRWISE_ROLE.md` 宣告的角色評分。
4. 若同時提交兩個 Pairwise skill，未宣告的另一個 skill 會被忽略。
5. 若 `PAIRWISE_ROLE.md` 缺漏、格式錯誤或 `skill_path` 不存在，Pairwise Track 視為無法評分，該 Track 0 分。

#### Pairwise 配對公平性

為避免分數受隨機對手品質過度影響，Pairwise 計分採以下原則：

1. **Code Author 分數只由其 code 在 hidden tests 上的表現決定**，不受配對 Bug Hunter 品質影響。
2. **Bug Hunter 分數由三部分組成**：
   - 50%：staff reference buggy code
   - 25%：staff reference clean code
   - 25%：學生 Code Author code
3. 對學生 Code Author code 的部分，評分器會以固定 random seed，為每個 Bug Hunter 抽取 `K` 個不同 Code Author 輸出進行評估；`K` 以 starter repo 或課程公告為準。
4. 若可用 Code Author 數量不足，則以 staff reference author 補足。
5. random seed、配對清單與每次執行 log 會在評分後保存，供查核。

> [!TIP]
> **提示**
> **為什麼是兩個 skill 而非 subagent？** 對應課程「Skill vs. Sub-Agent」的預設原則：Pairwise 的兩個角色各自是 stateless、固定 schema 的工作，用兩個 skill 最貼切；subagent（自主多步迴圈）留給 Open Track 真正需要時再用。

#### Skill A — Code Author

- 輸入：程式任務描述 + 限制（允許/禁止的 import、entry function 名稱）。
- `scripts/` harness：跑 sample 輸入自測、以 `radon raw` 計算 SLOC、檢查禁用 import。
- 輸出契約：`code`、`loc`、`self_test_results`、`rationale`、`confidence`。
- 限制：最多 500 S-LOC Python（Source Lines of Code，排除空行與純註解行；以 `radon raw` 計算）。

##### Code Author sandbox

評分器會在 sandbox 中執行 Code Author 輸出的 code：

- Python version：3.11.x（以 starter repo Docker image / grading image 為準）。
- 執行方式：評分器會將 `code` 寫入單一 `.py` 檔，import 後呼叫 constraints 指定的 `entry_function`。
- 禁止 network access。
- 禁止讀寫目前工作目錄以外的檔案。
- 禁止使用 `subprocess`、`multiprocessing`、`threading` 建立外部程序或長時間背景工作。
- 禁止動態 import：`__import__`、`importlib.import_module`、以 `eval` / `exec` 產生 import 均視為違規。
- timeout：每個 hidden test case 5 秒；超時則該 test case fail。若初始化 import 即超時，該 scenario 0 分。
- memory limit：512 MB；超過視為 runtime failure。
- S-LOC 以 starter repo 指定版本之 `radon raw <file> --json` 結果中 `sloc` 欄位為準。評分器不另行人工判斷空行、註解或 docstring。
- 輸出契約中的 `loc` 欄位為 skill 自行回報之參考值；正式 LoC 判定以評分器重新執行 `radon raw` 的結果為準。若學生回報之 `loc` 與評分器計算結果不一致，不會單獨扣分，但若評分器計算結果超過 500 S-LOC，仍依超限規則處理。

#### Skill B — Bug Hunter

- 輸入：Code Author 的輸出（code + 原始任務描述）。
- `scripts/` harness：可做靜態分析（如 `ast`）、構造邊界輸入。
- 輸出契約：結構化 bug report（行號、severity、type、suggested_fix）。
- 目標：精確指出 bug，且不誤報乾淨 code。

##### Bug Hunter 行號定義

Bug Hunter 的 `line_start` / `line_end` 依以下規則判定：

- 行號以 Code Author JSON 中 `code` 字串為唯一基準。
- 評分器會先將 `\r\n` 正規化為 `\n`，但不會刪除 code 內部空行。
- 行號採 1-indexed。
- 空行與註解行都計入行號。
- `line_start` / `line_end` 必須指向造成 bug 的最小相關程式區段；若 bug 橫跨多行，可回報範圍。
- 評分器不會以測試 harness wrapper 的行號作為比對基準。

##### `bug.type` 說明

`bug.type` 須從下列擇一；填入非清單內的值視為輸出契約違規。

| type | 意思 | 典型例子 |
| --- | --- | --- |
| `off_by_one` | 索引或邊界差一 | 迴圈用 `range(n-1)` 漏掉最後一個元素、`<` 與 `<=` 用錯 |
| `null_deref` | 對 None / 空值取用屬性或索引 | 沒檢查就 `obj.attr`，而 `obj` 可能是 `None` |
| `type_error` | 型別不符或誤用 | 把 `str` 當 `int` 運算、對 `None` 做 `len()` |
| `logic_error` | 邏輯錯誤，演算法本身想錯 | 條件判斷寫反、該用 AND 卻用 OR、回傳錯的變數 |
| `edge_case` | 邊界情境未處理 | 空輸入、單一元素、極大/負數、重複值 |
| `api_misuse` | 誤用函式庫或內建 API | 參數順序錯、用了被棄用的方法、回傳值理解錯誤 |
| `inefficient` | 結果正確但效能不佳 | 該用 O(n) 卻寫成 O(n²)、重複計算可快取的值 |
| `unhandled_input` | 未驗證或未處理的非法輸入 | 沒檢查格式就直接解析、未對非法參數 raise |

##### `severity` 說明

`severity` 須從下列擇一：

| severity | 意思 |
| --- | --- |
| `critical` | 必定導致錯誤結果或程式崩潰，且影響核心功能 |
| `high` | 在常見輸入下就會出錯 |
| `medium` | 僅在特定 / 邊界情境下出錯 |
| `low` | 不影響正確性，屬於風格、效能或可讀性問題 |

> [!TIP]
> **提示**
> **如何判斷 severity**：把問題想成「多容易被觸發、後果多嚴重」。空輸入才會炸的 bug 通常是 `medium`（邊界才觸發）；任何正常輸入都會回傳錯誤答案的 bug 則是 `high` 或 `critical`。注意：**把風格問題標成 `high` 會在評分時因 severity 校準不準而扣分** —— 嚴重度要與實際影響相符。

#### Pairwise 互動流程

```
sequenceDiagram
  participant E as 評分環境
  participant H as Hermes Agent
  participant A as Skill A (Code Author)
  participant B as Skill B (Bug Hunter)

  E->>H: hermes chat -q /code-author {task_desc, constraints}
  H->>A: 載入 skill，產生 code + 自測
  A-->>E: 結構化輸出 {code, loc, self_test, rationale}
  E->>H: hermes chat -q /bug-hunter {code, task_desc}
  H->>B: 載入 skill，靜態分析 + LLM 審查
  B-->>E: 結構化輸出 {bugs[], verdict, confidence}
  E->>E: 對 A 跑 hidden tests · 比對 B 的 bug 是否對應實際 failure · 雙方各自計分
```
圖 2 — 評分環境串接 Code Author 與 Bug Hunter 兩個 skill

*圖 2 — 評分環境串接 Code Author 與 Bug Hunter 兩個 skill*

#### 完整範例：一個 scenario 從頭到尾

示範 `task_042`（實作 `merge_intervals`）。

**① 評分環境呼叫 Code Author skill**：

```bash
hermes chat --toolsets skills -q '/code-author-annahsu041 {"task_id":"task_042","task_description":"Implement merge_intervals(intervals): merge overlapping intervals, empty input returns [].","constraints":{"entry_function":"merge_intervals","max_loc":500,"imports_forbidden":["os","sys"]}}'
```

**② Skill A 輸出**（此例 Author 漏了空輸入 edge case）：

```json
{
  "task_id": "task_042",
  "code": "from typing import List\ndef merge_intervals(intervals):\n    intervals.sort(key=lambda x: x[0])\n    merged = [intervals[0]]\n    for cur in intervals[1:]:\n        if cur[0] <= merged[-1][1]:\n            merged[-1][1] = max(merged[-1][1], cur[1])\n        else:\n            merged.append(cur)\n    return merged",
  "loc": 9,
  "self_test_results": {"passed": 1, "failed": 0},
  "rationale": "Sort then sweep.",
  "confidence": 0.85
}
```

> 這段 code 在一般輸入正確，但**空輸入 `[]` 會在 `intervals[0]` 崩潰**。Author 的自測沒涵蓋空輸入，所以沒發現。

**③ 評分環境把 A 的輸出餵給 Bug Hunter skill**：

```bash
hermes chat --toolsets skills -q '/bug-hunter-annahsu041 {"task_id":"task_042","code":"...","task_description":"...empty input returns []."}'
```

**④ Skill B 輸出**（成功抓到 edge case）：

```json
{
  "task_id": "task_042",
  "verdict": "buggy",
  "bugs": [
    {
      "line_start": 4,
      "line_end": 4,
      "severity": "medium",
      "type": "edge_case",
      "description": "Empty intervals raises IndexError; spec requires returning [].",
      "suggested_fix": "Guard: if not intervals: return []."
    }
  ],
  "confidence": 0.8
}
```

**⑤ 評分環境對兩個 skill 分別計分**：

| Skill | 評分依據 | 此例結果 |
| --- | --- | --- |
| **A（Code Author）** | code 跑 hidden test cases（含空輸入那筆） | 空輸入該題 fail → 失一分；其餘通過 |
| **B（Bug Hunter）** | 報的 bug 是否對應 A 的實際 failure（行號 + 類型） | 正確指出空輸入、行號相符、type=`edge_case` 合理 → 得分 |

> [!TIP]
> **提示**
> **教學點**：A 的自測不周全（沒測空輸入），被 hidden test 抓到、也被 B 抓到。好的 Code Author skill 會在 `scripts/` 自動生成邊界測試自測；好的 Bug Hunter skill 會在 `scripts/` 主動構造邊界輸入去打對方的 code。兩邊都印證：deterministic 的邊界檢查，遠比單純相信 LLM 一次寫對更可靠。

### 2.4 Open Track（必做，40%）

Open Track 是本專案**佔分最高、也是必做的核心題目**。它讓你自由發想一個有意思的 skill —— 由你決定要做什麼、如何呼叫、用什麼 metric 證明它有效。因為 Basic / Pairwise 是固定題，**Open Track 是你能展現獨立工程判斷與差異化作品的唯一舞台**，請務必認真投入。

**不需事先送審核** —— 你只要在 repo 根目錄放一份固定格式的宣告檔 `OPEN_TRACK.md`，評分時我們會以課程指定的 LLM judge 與 deterministic checker 判定其合規性，並依你宣告的呼叫方式在課程 Hermes 上執行你的 skill。

> [!WARNING]
> **注意**
> **Open Track 不因「概念新穎」給分。** 若 `OPEN_TRACK.md` 無法回答「metric 是什麼、如何驗證」，將判定為不可評分。Open Track 的精神為 **open in design, strict in verification**。

#### `OPEN_TRACK.md` 必填格式

請完整填寫以下七個區塊。標題請照抄，方便自動解析。

```markdown
## 1. Skill 簡介
（一句話說明你的 skill 做什麼）

## 2. Skill 名稱與目錄
（你的 skill 在 repo 中的路徑，例如 skills/open-mytool-annahsu041/）

## 3. 呼叫方式
（評分環境要如何以 hermes chat -q 呼叫你的 skill：slash command、輸入 JSON 範例、
 預期輸出 JSON 範例。請寫到「照著就能跑」的程度，judge 會依此推導呼叫序列。）

## 4. 自定 Verifiable Scenario
（你用什麼 scenario 證明 skill 有效？評分 metric 是什麼？
 並論證此 metric 為何不可 gameable —— 例如結果可程式化比對、有 ground truth、無法靠亂猜取分。）

## 5. 預期失敗模式
（列出至少 2 種預期會遇到的失敗，可參考 §4.4 的 MAST 分類，說明觸發點與處理方式。）

## 6. 互動對象
（你的 skill 會跟誰互動？可以是 staff reference skill、Basic/Pairwise 的 skill，
 或——若你和其他同學彼此認識——對方的 skill。詳見下方「跨 skill 協作」。
 若需多步自主推理，可使用 Hermes 的 subagent，請在此說明。）

## 7. Token Budget 估算
（預估每個 scenario 的 token 消耗；若 > 50k tokens/scenario，請附理由。）
```

#### Open Track verifiability 要求

Open Track 的 verifiable scenario 必須包含：

1. **Public scenario**：學生在 `OPEN_TRACK.md` 中提供至少 3 個可執行範例。
2. **Deterministic evaluator**：學生需提供或描述可程式化比對方式。
3. **Ground truth 或客觀判定標準**：例如固定答案、可執行測試、schema check、hash / diff、unit tests、property-based checks、reference output 等。
4. **Staff perturbation**：評分時，課程可在不改變任務本質的前提下，產生若干變體輸入，例如改變資料順序、替換等價名稱、加入無關干擾項、調整邊界值。
5. **Anti-hardcoding**：若 skill 只能對 `OPEN_TRACK.md` 中的固定字串或固定 `task_id` 正確輸出，對 staff perturbation 失敗，則視為 metric gameable，Open Track scenario 表現分數可為 0。

`OPEN_TRACK.md` 中必須明確說明：

- ground truth 從何而來；
- 評分器如何自動判定 pass/fail；
- 哪些輸入變化仍應被視為同一任務能力；
- 為何固定輸出、關鍵字比對或人工主觀判斷無法取得高分。

#### 自動合規判定與 report

評分時，合規判定會讀取 `OPEN_TRACK.md` 並檢查：

1. 七個區塊是否齊全；
2. skill path 是否存在；
3. skill 是否能裝進 Hermes 並被呼叫；
4. 呼叫方式是否清楚到可被推導執行；
5. 自定 metric 是否真的可驗證且不可 gameable；
6. 輸出 schema 是否足以被自動解析與評分。

合規判定會產生 machine-readable report，至少包含：

- 是否通過七區塊格式檢查；
- 找到的 skill path；
- 推導出的 `hermes chat` 呼叫方式；
- 判定 metric 是否可驗證；
- 若不通過，列出不通過原因與對應區塊。

合規判定由 LLM judge 輔助，但最終以評分器產生的 report 為準。課程保留人工覆核明顯工具錯誤的權利；但學生不得以 deadline 後未寫在 repo 內的資訊補充說明。

#### 跨 skill 協作（鼓勵）

我們**特別歡迎**彼此認識的同學，讓各自的 skill 在同一個 Hermes Agent 上互相呼叫、共同呈現成果 —— 這正是 multi-agent 系統最有趣的地方。若你想這麼做：

- 在「## 6. 互動對象」中**明確寫出你要呼叫的對方 skill 名稱**，以及預期互動流程。
- 雙方都需各自在自己的 `OPEN_TRACK.md` 中宣告這段協作，評分環境才能正確接線。
- 協作成果仍須各自滿足「自定 verifiable scenario」—— 即使是合作，每個 skill 的貢獻仍要能被獨立驗證，而非「兩個 skill 互相吹捧就算過」。

跨 skill 協作不等於共同開發。允許雙方公開各自 skill 的呼叫介面、輸入輸出 schema 與互動流程；但不得共寫或互相複製 `SKILL.md`、`scripts/`、prompt template、evaluator 或可直接提交的實作。每位學生仍需能獨立說明自己 skill 的設計與貢獻。

---

## 三、繳交規定

### 3.1 必繳檔案結構

repo 即是一個可被 Hermes 安裝的 skill tap（`skills/` 下每個資料夾為一個 skill）：

```text
aiase-2026-final-annahsu041/
├── skills/
│   ├── text2sql-annahsu041/             # Basic Track，必交
│   │   ├── SKILL.md                      # 必要
│   │   └── scripts/                      # 你的 harness（run.py 等）
│   ├── code-author-annahsu041/          # Pairwise，若選 Code Author
│   │   ├── SKILL.md
│   │   └── scripts/
│   ├── bug-hunter-annahsu041/           # Pairwise，若選 Bug Hunter
│   │   ├── SKILL.md
│   │   └── scripts/
│   └── open-<short-name>-annahsu041/    # Open Track，必交
│       ├── SKILL.md
│       └── scripts/
├── dev_set/                              # 課程提供之公開 dev set（含答案）供本地自測
├── run_dev.py                            # 本地自測：驅動 hermes chat -q 跑 dev set 並比對
├── PAIRWISE_ROLE.md                      # Pairwise 角色宣告，必交
├── OPEN_TRACK.md                         # Open Track 宣告，必交
└── report.md                             # 期末報告，必交
```

Open Track 可以重用 Basic / Pairwise skill 作為子流程，但仍須在 `OPEN_TRACK.md` 中指定一個主要受評 skill path。

### 3.2 Repo 權限規定

- 所有學生 repo 為 **private**，由 GitHub Classroom 自動建於 `aiase-2026` course org 之下。
- 學生為自己 repo 之 admin；TA team 具 read + write 權限。
- **評分時，課程將於 deadline 後一次性把全部學生 repo clone 至地端**，於課程的 Hermes Agent 上安裝、執行、評分，不再連回 GitHub。
- 學生**互相之間不可見**對方 repo。

### 3.3 評分執行流程

評分於 **2026/6/17 在課程的 Hermes Agent 上一次性執行**，流程如下：

1. **Clone 全部 repo 至地端**：deadline 一過，課程把全部學生 repo clone 至地端，並記錄每個 repo 的 URL、default branch、git commit SHA 與 clone timestamp 作為 audit 證據。此後任何 GitHub commit 皆不影響評分。
2. **安裝 skill**：把每位學生 `skills/` 下的 skill 安裝進課程 Hermes 的 `~/.hermes/skills/`（等同 `hermes skills install`）。
3. **安裝 Python dependencies**：若 skill 目錄下有 `scripts/requirements.txt`，依 §1.6 規則安裝。
4. **Security scan**：安裝時會經過 Hermes 內建的 security 掃描；含危險操作（破壞性指令、資料外洩、prompt injection 等）者會被擋下並記錄。
5. **執行 hidden scenarios**：以 `hermes chat --toolsets skills -q` 對每個 skill 餵入 hidden 任務；Pairwise 題目則串接對向 skill 或 staff reference skill。
6. **擷取 JSON**：擷取每次執行的最後一個 fenced JSON 區塊，並做 schema validation。
7. **計分**：對 hidden set / Open Track metric 自動比對，計算分數，產出 scoreboard 與 grading report。

> [!WARNING]
> **注意**
> **程式正確性是你的責任。** 本專案**不提供 CI 自動檢查**。繳交前，請務必在你自己本地安裝的 Hermes Agent 上，實際以 `/skill-name` 或 `hermes chat -q` 確認你的 skill 能被載入、能正常產生符合輸出契約的結果。若 6/17 評分時你的 skill 裝不起來、無法被呼叫、或輸出不符契約，該部分將無法得分 —— 沒有事後補救機會。

### 3.4 Demo Day 定義

本專案之 Demo Day 指課程於 2026/6/17 使用統一 Hermes Agent 評分環境執行全班 skill，並展示部分代表性成果。除非課程另行公告，學生不需於 Demo Day 現場重新操作、口頭報告或補交檔案。Demo Day 當天無法以口頭說明修正 repo 中缺漏的資訊。

---

## 四、評分標準

總分 **100 分**，配置如下：

| 項目 | 配分 | 評分方式 |
| --- | --- | --- |
| Basic Track（必做） | 30 | Hidden test 自動評分 |
| Pairwise Track（必做） | 20 | 自動評分；依 `PAIRWISE_ROLE.md` 宣告角色計分 |
| Open Track（必做） | 40 | 合規 gate（pass/fail）+ scenario 70% + 互動 log 30% |
| 報告 + Demo Day | 10 | 設計決策與失敗分析深度 |

> [!NOTE]
> **重點**
> **評分模型 held-out 且全班統一。** 評分當次，全班所有 skill 一律在同一個正式計分模型、同一 Hermes 版本、同一評分環境下執行。實際用哪顆正式模型於評分前不公布（見 §1.7）。

### 4.1 Basic Track 評分（30 分）

- **輸出契約 conformance**（pass/fail gate）：skill 裝不起來、無法被呼叫、或最終輸出不是合法的契約 JSON，該 Track 0 分。
- **Hidden set accuracy**：`score = (passed_tasks / total_tasks) × 30`。
- Hidden set 約 100 題，dev set 提供 20 題（含答案）供開發。
- 比對方式為 **order-insensitive bag equality（multiset equality）**：列的順序不計，但重複列的次數會計入。也就是說，`[(Alice), (Bob)]` 與 `[(Bob), (Alice)]` 視為相同；但 `[(Alice), (Bob), (Bob)]` 與 `[(Alice), (Bob)]` 視為不同。
- 若題目語意要求去重，學生產出的 SQL 須自行使用 `DISTINCT` 或其他等價方法處理；評分器不會自動去重。

> [!TIP]
> **提示**
> **此 metric 不可 gameable**：hidden DB 內容不可見（無法猜答案）、SQL 須語法正確且可執行（無法抄關鍵字）、結果採 bag equality（無法靠排序或重複列碰運氣）。metric 與產出物之因果鏈越短，gameable 空間越小。

### 4.2 Pairwise Track 評分（20 分）

Pairwise Track 依 `PAIRWISE_ROLE.md` 宣告的角色評分。

#### Skill A — Code Author

- 將輸出的 code 置入 sandbox 執行 hidden test cases（每題約 10 個）。
- 分數 = `(passed_tests / total_tests)` 跨 scenarios 加總。
- 違反 LoC 上限、使用禁止 import、執行超時、記憶體超限、runtime crash：依規則該 test case 或 scenario 0 分。
- Code Author 分數只取決於自己輸出的 code，不受配對 Bug Hunter 品質影響。

#### Skill B — Bug Hunter

Bug Hunter 對三組 code 評分後加權平均：

| 對象 | 權重 | 衡量指標 | 用意 |
| --- | --- | --- | --- |
| Staff reference buggy code | 50% | Bug detection F1（行號精確比對） | 測 recall |
| Staff reference clean code | 25% | False positive rate | 測誤報 |
| 學生 Code Author code | 25% | B 報的 bug 是否對應 A 之實際 hidden-test failure（以最小觸發 input 與行號比對） | 測實戰準確度 |

加分項：`bug.type` 分類正確 + `suggested_fix` 經 judge 認定可行。

設計限制：永遠報一堆 bug → false positive rate 懲罰；永遠報乾淨 → recall 歸零。須具備真實 code review 能力方能得高分。

### 4.3 Open Track 評分（40 分）

| 項目 | 權重 | 評分方式 |
| --- | --- | --- |
| 合規判定（gate） | pass/fail | 七區塊齊全、skill 可裝進 Hermes 並被呼叫、呼叫方式可推導執行、metric 可驗證且不可 gameable。不過門檻直接 0 分。 |
| 自定 scenario 表現 | 70% | 按 `OPEN_TRACK.md` 宣告之 metric 與 staff perturbation 自動評分。 |
| 互動 log 品質 | 30% | 是否確實在 Hermes 上完成 skill 工作；若宣告跨 skill 協作，需有雙向互動或明確資料流證據。 |

Open Track 的 `OPEN_TRACK.md` 會作為合規與 metric 判定依據；`report.md` 則在 §4.4 獨立計分，不與 Open Track 重複計算。

### 4.4 報告 + Demo Day（10 分）

`report.md` 須包含：

1. **設計決策**：`SKILL.md` 怎麼寫、harness 放了什麼、為何這樣設計。
2. **實際遭遇之失敗及其分析**：須附執行 log 證據；重點不在「有沒有失敗」，而在「能否說清楚失敗的成因」。
3. **改進方向**：若再做一次，會如何改善 skill、harness、metric 或測試流程。
4. **若為兩人組**：需說明 proposal 原分工與實際分工。
5. **引用說明**：若參考、改寫或借用 public code / skill / AI 產出，須依 §6 說明來源與差異。

配分建議：

| 項目 | 分數 |
| --- | --- |
| 設計決策清楚且與 verifiability 對應 | 3 |
| 失敗分析具體，且有 log 證據 | 5 |
| 改進方向可執行 | 2 |

> [!NOTE]
> **參考**
> **參考框架：MAST taxonomy（選用，非必要）**

本專案常見之失敗情境：

| 失敗情境 | 屬於 MAST 類別 | 典型觸發點 |
| --- | --- | --- |
| skill 未照規格 | (1) 規格與角色 | Code Author 之 code 未使用指定 entry function 名稱 |
| 資訊傳遞不足 | (2) agent 間協調 | Code Author 之 rationale 未陳述真實設計決定，致 Bug Hunter 誤判 |
| 驗證判斷錯誤 | (3) 驗證與品質 | Bug Hunter 對 code 給出錯誤 bug judgement（誤報或漏報） |
| 輸出契約失敗 | (3) 驗證與品質 | 最後輸出非合法 fenced JSON，或多輸出一段 JSON 導致評分器擷取錯誤 |
| Open Track metric gameable | (1)/(3) 規格與驗證 | skill 只對固定 task_id 回硬編碼答案，對 staff perturbation 失敗 |

---

## 五、開發與測試環境

**程式正確性是學生的責任** —— 本專案不提供 CI 自動檢查。你必須在**自己本地安裝的 Hermes Agent** 上完成開發與自測，確保 skill 能被載入、能正常產生符合輸出契約的結果。本地環境與評分環境用的是同一套 Hermes Agent，差異在資料來源（dev set vs hidden set）、評分模型選擇與評分器權限。

### 5.1 版本鎖定

本專案所有 Hermes CLI 行為、skill 載入方式、security scan 與評分流程，以 starter repo 指定之 Hermes Agent commit / release 版本為準。若官方最新版文件與 starter repo 指定版本不一致，請以 starter repo 為準。

### 5.2 安裝 Hermes Agent 並設定模型

在你自己的機器（Linux / macOS / WSL2）安裝 Hermes Agent。實際安裝方式以 starter repo 指令為準，範例如下：

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
source ~/.bashrc        # 重新載入 shell（或 source ~/.zshrc）
hermes doctor           # 檢查安裝是否正常
```

接著把 Hermes 的模型 provider 指向**課程的 LiteLLM Gateway**（OpenAI-compatible endpoint）。精確的 `~/.hermes/config.yaml` / `.env` 設定值會放在 starter repo —— 照著貼上即可，**不需自備任何 API key**。設好後以 `hermes model` 確認當前模型。

### 5.3 開發你的 skill 並接進 Hermes

兩種方式擇一：

- **方式 A（建議）**：在 `~/.hermes/config.yaml` 的 `skills.external_dirs` 加入你的 repo `skills/` 路徑，Hermes 會直接掃描你 repo 內的 skill，邊改邊測、不必複製。
- **方式 B**：把 skill 資料夾複製到 `~/.hermes/skills/` 下。

裝好後，`hermes skills list` 應能看到你的 skill；在 `hermes` 互動介面打 `/text2sql-annahsu041` 即可觸發。

### 5.4 本地自測

三種層次：

```bash
# (1) 互動式單題測試
hermes                         # 進入 CLI，輸入 /text2sql-annahsu041 {...} 觀察輸出

# (2) 非互動式單題（與評分環境同一條路徑）
hermes chat --toolsets skills -q '/text2sql-annahsu041 {"task_id":"...","question":"...","db_schema":"...","dialect":"sqlite"}'

# (3) 批次自測：對整份 dev set 跑一遍並自動比對（starter repo 附）
python run_dev.py              # 驅動 hermes chat -q 跑 dev_set/、擷取 JSON、與答案比對、印出 pass/fail
```

> [!NOTE]
> **重點**
> **dev set 含答案，hidden set 不含。** `run_dev.py` 能在本地算出你在 dev set 上的 pass rate，是你唯一可靠的自我檢驗工具。評分用的 hidden set 永遠不會給你答案。

### 5.5 Reference Skills（Pairwise 對手）

Pairwise 題之 skill 須對課程提供之多種策略對手測試（皆可從 starter repo 安裝）：

**供 Code Author 測試之 Bug Hunter**：

- `reference-bug-hunter-conservative`：低誤報。
- `reference-bug-hunter-aggressive`：任何 edge case 皆報。
- `reference-bug-hunter-noisy`：30% 隨機誤報，模擬不可靠對手。

**供 Bug Hunter 測試之 Code Author**：

- `reference-author-clean`：乾淨 code，不應報 bug。
- `reference-author-buggy`：明顯 bug，須全抓。
- `reference-author-tricky`：subtle bug，為高分指標。

### 5.6 用量額度與開發策略

課程透過 LiteLLM Gateway 為**每位同學**設定 **2 美元** 的 API 成本上限（涵蓋整個開發期的付費模型呼叫；評分期由課程於地端另行控管，不佔用你的額度）。

> [!NOTE]
> **重點**
> **開發期只提供 `gemma4` 與 `gemini-2.5-flash`。** `claude-haiku-4-5` 只在 optional robustness run 階段才可能被投入（見 §1.7），開發期不對學生開放、無法透過 LiteLLM 取得。這正是 held-out 的用意 —— 你無法事先針對它調校，只能把 skill 做到 model-agnostic。

| 模型 | 開發期是否可用 | 計費 | 用途 |
| --- | --- | --- | --- |
| `gemma4`（本地模型） | ✅ 可用 | 不計費（課程自架） | 基礎開發、反覆迭代、debug |
| `gemini-2.5-flash` | ✅ 可用 | 計入你的 2 美元上限 | 跨模型自我驗證階段 |
| `claude-haiku-4-5` | ❌ 僅 optional robustness run | 不適用（學生開發期取不到） | held-out 穩健性展示，⭐ 標註用 |

**建議策略 —— 先 Gemma，後付費模型：**

1. **基礎開發階段：以 `gemma4` 為主**。把 SKILL.md、scripts/ harness、retry、輸出契約全部做穩。不計費，可多次 `run_dev.py` 迭代，不要在這階段動用付費額度。
2. **自行驗證階段**：基礎穩了，再 `hermes model` 切到 `gemini-2.5-flash` 跑一輪，確認你的 skill 不是只對 Gemma 有效。由於 optional robustness run 可能抽到開發期沒見過的模型，請把重點放在「不依賴特定模型脾氣」的防禦性設計，而非針對某顆模型微調。

> [!NOTE]
> **重點**
> **2 美元上限用完不補。** 別在基礎開發階段就燒付費額度，請留給「驗證跨模型穩健性」這個真正需要它的階段 —— 基礎開發用免費的 `gemma4` 就夠了。

### 5.7 繳交前自我檢查清單

繳交前請確認：

- [ ] default branch 上已有最終版本。
- [ ] skill folder name 與 `SKILL.md` frontmatter `name` 一致。
- [ ] `hermes skills list` 看得到你的 skill。
- [ ] `hermes chat --toolsets skills -q '/skill-name {...}'` 可執行。
- [ ] 最後輸出為單一合法 fenced JSON block。
- [ ] `task_id` 與輸入一致。
- [ ] Basic Track 可跑完 `python run_dev.py`。
- [ ] Pairwise 已在 `PAIRWISE_ROLE.md` 宣告角色。
- [ ] Open Track 已填完 `OPEN_TRACK.md` 七個固定 heading。
- [ ] Open Track 至少提供 3 個 public scenarios，且 metric 可自動驗證。
- [ ] 所有非標準函式庫已寫入 `scripts/requirements.txt`。
- [ ] 無 hardcoded absolute path、個人 API key、外部 MCP server 或外部網路依賴。
- [ ] `report.md` 含設計決策、執行 log 摘要、失敗分析、改進方向與引用說明。

### 5.8 評分器 gate 清單

評分器會依序檢查：

- repo clone success
- default branch resolved
- required files exist
- skill install success
- dependency install success
- skill callable
- stdout contains valid final fenced JSON
- JSON schema valid
- security scan pass
- runtime within timeout
- hidden / Open Track evaluator completed

任一 gate 失敗，對應 Track 可能無法得分。

---

## 六、學術誠信

- 本專案為**個人作業**。可討論架構、skill 設計、debug 思路；**不得共寫 SKILL.md / scripts 或共用可直接提交的 prompt template**。
- Pairwise 題之配對由課程自動指派，**不得**與同學私下約定配對以影響評分。
- 若偵測到兩份 skill 高度相似，依學術誠信規定處理。
- 嘗試在 skill 中以網路請求或 file system 存取 hidden set 內容者，Hermes 的 security 掃描與 sandbox 會擋下並記錄，以 0 分處理。
- 成績公布後，學生可自行 fork 至個人帳號並設為 public 以作為作品集，或發佈為自己的 skill tap。

### 6.1 AI 輔助使用政策

- 允許使用 AI coding assistants 協助理解錯誤、產生草稿、撰寫測試或改善文字。
- 學生需對最終提交內容完全負責，包括 correctness、security、license 與引用。
- 不需逐條揭露一般 AI 輔助對話；但若 AI 產出的內容明顯改寫自特定 public repo、文章、skill 或第三方程式碼，仍須依 §6.2 註明來源。
- 禁止與其他學生共用完整 SKILL.md、scripts、prompt template、Open Track evaluator 或可直接提交的實作。

### 6.2 關於參考網路上的 skill / agent code

網路上有大量現成的 skill 與 agent 程式碼可供參考（Hermes 本身就整合了多個 skill tap），**我們鼓勵你站在前人的基礎上學習**。但使用時請務必遵守：

- **務必註明引用來源與差異**：若你的 SKILL.md 或 scripts 參考、改寫或借用了任何 public code / skill，請在程式碼或 `report.md` 中明確註記**出處**（repo 連結 / 作者），並說明**你的版本與原版的差異**。
- **我們會 clone 全部同學的程式並建立比對清單**，保留於課程 repo。
- **AI 自動比對未註明之引用**：我們會請 AI 對全部提交與 public code 做相似度比對。若你的程式與某份 public code 高度相似卻未加註引用，AI 將在該段程式後方以紅字標註「未註明的引用（undeclared reference）」。有正當註明的引用不受影響；真正會被檢視的是「明明參考了卻不說」。
- AI similarity report 僅作為初步標記；是否構成違規，仍由課程依原始碼、引用說明、commit history 與學生說明綜合判定。

> [!TIP]
> **提示**
> **誠信的引用不會扣分，隱藏的引用才會。** 工程師站在巨人肩膀上是常態 —— 重點不是「你有沒有參考別人」，而是「你有沒有誠實說明、並展現你在其上的理解與改造」。清楚的引用與差異說明，本身就是工程能力的一部分。

### 6.3 成果公開範圍

課程可能公開：

- 本次專案整體成果摘要與統計；
- 經課程挑選之優秀作品名稱、簡介、demo log 或截圖；
- 經學生同意後公開之 repo / skill tap 連結。

課程不會在未另行告知或未取得必要授權前，公開所有 private repo 原始碼。若需公開個人姓名、學號或 GitHub ID，將依課程與學校相關規範處理。

---

## 七、時程

所有 deadline 皆以 **Asia/Taipei（UTC+8）** 時間為準。

| 階段 | 截止時間 |
| --- | --- |
| **Team-of-Two proposal（如要組 2 人團隊）** | 2026/6/2 23:59 |
| **最終繳交（skills + report）** | **2026/6/16 23:59** |
| **Demo Day（於課程 Hermes Agent 評分）** | 2026/6/17 上課時間 |

---

## 八、參考資源

### 課程概念

- Harness Engineering — deterministic shell 之設計（你的 `scripts/`）。
- Spec-Driven Development — 把 `SKILL.md` 當合約。
- Verifiability Mindset — metric 為何不可 gameable。
- Context Engineering — `SKILL.md` 即 skill 與 agent 間之合約。
- Skill vs. Sub-Agent — 預設用 Skill，subagent 留給真正需要多步自主推理時。
- MAST Taxonomy — multi-agent 失敗分類詞彙（報告選用，見 §4.4）。

### Hermes Agent 與 Skill 標準

- [Hermes Agent（GitHub）](https://github.com/NousResearch/hermes-agent) — 本專案的 agent 平台。
- [Hermes Agent 官方文件](https://hermes-agent.nousresearch.com/docs/) — 安裝、CLI、模型設定。
- [Skills System 文件](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills) — `SKILL.md` 格式、目錄結構、安裝。
- [agentskills.io](https://agentskills.io) — Skill 開放標準。
- `garrytan/gstack`、`openai/skills`、`anthropics/skills` — Hermes 內建可參考的 skill tap。

### 外部資源

- MAST taxonomy 相關論文與課程補充資料 — multi-agent 失敗分類詞彙。
- `karpathy/autoresearch` — verifiability metric (`val_bpb`) 之典範實作。

---

## 結語：成果發表與對你的意義

完成後，我們會將本次期末的整體成果，透過 **TAICA（臺灣人工智慧卓越中心聯盟課程平台）對外宣布**。這代表你的努力不只是一份課堂作業，而會成為一個公開、可被看見的工程成果 —— 你做出來的是能裝進真實 Hermes Agent、別人也能用的 skill。

這個專案刻意做得比一般作業大、也更接近真實世界 —— 從為真實 agent 平台寫 skill、harness engineering、跨模型穩健性，到誠實的引用與失敗分析，每一項都是你未來在業界或研究中會反覆用到的能力。

> 希望這個專案能成為大家未來的助力！ 🚀

---

*AIASE 2026 期末專案規格書 · NCKU CSIE · 莊坤達*

