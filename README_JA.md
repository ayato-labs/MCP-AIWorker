# MCP-AIWorker: トークン防壁 (Tokenizer Barrier) インフラ

[![CI](https://github.com/ayato-labs/MCP-AIWorker/actions/workflows/ci.yml/badge.svg)](https://github.com/ayato-labs/MCP-AIWorker/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English Version is here](README.md)

**MCP-AIWorker** は、あらゆるAIエージェントシステムにおいてトークン消費を抑え、開発コストを劇的に下げるための高性能な **トークン防壁 (Tokenizer Barrier)** として機能するMCPサーバーです。

Claude Code、Cursor、または独自のカスタムエージェントなど、どのMCPクライアントからも利用可能です。MCP-AIWorkerは、定型的なコードの下書き作成、巨大なログ出力の要約、Webコンテンツの解析といった「知的判断は不要だがトークン消費が激しい作業」をインターセプトし、Gemini Flash 3.1などの安価かつ高速なサブモデルへ委譲します。

メインAI（Architect）は、高次元の意思決定とシステム設計に専念させることができます。

---

## 🛡️ なぜ「トークン防壁」が必要なのか？

エージェントがファイル全体の分析やビルド・実行ループを行うと、コンテキストウィンドウを一瞬で消費し、APIコストが膨れ上がります。MCP-AIWorker は **Architect-Worker（設計者と作業者）分業パラダイム** を適用することでこれを解決します。

*   **劇的なコスト削減**: 構造的なコーディング、翻訳、ログ解析を低コストモデルへオフロードします。
*   **コンテキスト汚染の防止**: 大量のログやWebページをそのままメインAIに渡さず、必要な要約のみを供給することでコンテキスト枠を節約します。
*   **予測可能なパフォーマンス**: 複雑で非決定的な内部QAループを意図的に排除し、Architect AIの判断速度を一定に保ちます。
*   **プラットフォーム非依存**: MCP準拠のクライアントであれば、あらゆる環境から利用可能です。

### トークン使用量の追跡とコスト監視 (Token Observatory)
MCP-AIWorkerには、コスト削減実績を証明するためのテレメトリ機能が組み込まれています。
1. 各ツール実行時のトークン消費量を自動的にSQLiteデータベースに蓄積します。
2. 以下のコマンドで、リアルタイムのコスト削減状況とトークン消費指標を確認できます：
```bash
.venv\Scripts\python.exe scripts\show_dashboard.py
```

---

## 🏗️ アーキテクチャ

```
                 +------------------------+
                 |       メインAI         |
                 |      (Architect)       |  <-- システム設計・最終検証
                 +-----------+------------+
                             |
                     MCP Tool Calls
                             v
                 +-----------+------------+
                 |      MCP-AIWorker      |  <-- トークン防壁
                 +-----------+------------+
                             |
             +---------------+---------------+
             |               |               |
             v               v               v
      +------------+   +------------+  +------------+
      |   Gemini   |   |   Ollama   |  |  Genspark  |  <-- 安価・ローカルLLM
      |   (API)    |   |  (ローカル)  |  |  (検索)    |      が泥臭いコーディング
      +------------+   +------------+  +------------+      やログ要約を担当
```

---

## 🚀 クイックスタート (Windows)

### 1. 環境構築
```bash
setup.bat
```

### 2. 環境変数の設定 (`.env`)
```env
AI_PROVIDER=gemini
GOOGLE_API_KEY=your-api-key-here
DRAFTING_MODEL=models/gemini-3.1-flash-lite
```

### 3. サーバーの起動
```bash
run.bat
```
サーバーが `http://127.0.0.1:10300/mcp` で起動します。

---

## 🛠️ 提供されるツール

| ツール | 役割 |
| :--- | :--- |
| `draft_edit` | 高速なコード下書き作成。 |
| `find_target` | リポジトリ全体を対象としたターゲット修正。 |
| `execute_command` | コマンド実行結果をAIエージェントに適した簡潔な要約に変換。 |
| `fetch_and_summarize_url` | トークン消費を抑えつつWebコンテンツを要約。 |
| `generate_unit_tests` | AAAパターンに基づいたユニットテスト生成。 |

---

## 📄 アーキテクチャ決定レコード (ADR)

本プロジェクトは厳格な設計指針に基づいています。[docs/ADR/](docs/ADR/) にあるADRをご一読ください。Gitコンフリクト解消や自動タスクルーティングといった「複雑さの温床となる機能」を意図的に実装しないことで、シンプルかつ高速な状態を維持しています。

---

## ⚖️ ライセンス

MIT License。詳細は [LICENSE](LICENSE) を参照してください。
