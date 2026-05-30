<!--
   Open Track 宣告 — 七個 heading 請照抄,順序也別動。
   合規判定會自動解析這七節;少一節就 fail gate。
   詳細要求見規格書 §2.4 與 §4.3。
-->

## 1. Skill 簡介

(一句話說明你的 skill 做什麼。)

## 2. Skill 名稱與目錄

(你的 skill 在 repo 中的路徑,例如 `skills/open-mytool-<github_id>/`。)

## 3. 呼叫方式

(評分環境要如何以 `hermes chat -q` 呼叫你的 skill。需包含:slash command、輸入 JSON 範例、預期輸出 JSON schema 範例。請寫到「照著就能跑」的程度。)

**Slash command:**

```
/open-<short-name>-<github_id>
```

**輸入 JSON 範例:**

```json
{
  "task_id": "open_example_001",
  "input": "..."
}
```

**輸出 JSON 範例(此即輸出 schema):**

```json
{
  "task_id": "open_example_001",
  "result": "...",
  "confidence": 0.0
}
```

## 4. 自定 Verifiable Scenario

(你用什麼 scenario 證明 skill 有效?評分 metric 是什麼?並論證此 metric 為何不可 gameable —— 例如結果可程式化比對、有 ground truth、無法靠亂猜取分。)

**Scenarios(請提供至少 3 個):**

- Scenario 1: ...
- Scenario 2: ...
- Scenario 3: ...

**Metric:** (描述評分器如何從輸出 JSON 自動算出分數,例如「`result` 欄位以 bag equality 比對 ground truth」或「以 SHA256 比對固定 reference output」。)

**為何不可 gameable:** (例如:ground truth 對學生不可見、staff perturbation 後仍可重現、無法靠關鍵字 / hardcoded 答案取分。)

## 5. 預期失敗模式

(列出至少 2 種預期會遇到的失敗。可參考規格書 §4.4 MAST taxonomy 的詞彙,說明觸發點與處理方式。)

- 失敗 1: ...(觸發點 / 處理)
- 失敗 2: ...(觸發點 / 處理)

## 6. 互動對象

(你的 skill 會跟誰互動?可以是 staff reference skill、Basic/Pairwise 的 skill,或其他同學的 skill(需雙方都宣告)。若需多步自主推理而用了 Hermes subagent,請在此說明 subagent 的觸發條件與終止條件。)

## 7. Token Budget 估算

(預估每個 scenario 的 token 消耗。若 > 50k tokens/scenario,請附理由。)

| Scenario | 預估 input tokens | 預估 output tokens | 預估 total |
|---|---:|---:|---:|
| Scenario 1 | | | |
| Scenario 2 | | | |
| Scenario 3 | | | |
