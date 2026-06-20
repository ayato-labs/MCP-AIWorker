# MCP-AIWorker 長期発展計画

## ビジョン
MCP-AIWorkerを「高性能AIの思考コストを最小化するためのAI Worker基盤」として発展させる。
目標はAgent構築ではなく、Claude Code, Cursor, Codex, Gemini CLIなどの高性能AIが消費するトークン、API料金、推論時間を削減することである。

## 基本方針
- **やること**: 高性能AIが読む情報量を減らす。
- **やらないこと**: 安価AIに意思決定させる。

## 設計原則
1. **Architect と Worker を分離する**: Architect(Claude, GPT, Gemini Pro)は指示し、Worker(Gemini Flash, Gemma, Qwen, Ollama)は作業のみを行う。Workerは考えない。
2. **AIを賢くしない**: Agent化、自己反省、自律実行は禁止。
3. **コスト削減量を定量化する**: 全機能は「何トークン削減したか」を評価軸とする。

## 開発フェーズ

| フェーズ | 名称 | 目的 | 優先度 |
| :--- | :--- | :--- | :--- |
| 1 | Token Observatory | 価値の可視化 (計測基盤) | S |
| 2 | Repository Intelligence | 対象探索精度向上 (Tree-sitter) | S |
| 3 | Semantic Search | grep依存脱却 (Vector Search) | A |
| 4 | Dependency Graph | 局所編集精度向上 (Code Graph) | A |
| 5 | Worker Parallelization | 処理速度向上 | B |
| 6 | Context Compression Engine | コンテキスト削減強化 | A |
| 7 | Cost Benchmark Suite | 優位性証明 | S |
| 8 | Enterprise Edition | 収益化 | B |

## 禁止事項 (差別化要因維持のため)
- Agent化
- 自律意思決定
- AutoGen化
- CrewAI化
- LangGraph化

---
目標は「最も賢いAIを作る」のではなく、「最も安く賢いAIを使う」ことである。
