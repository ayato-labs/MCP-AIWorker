# Sub-cheap-McpAiAgent

**Sub-cheap-McpAiAgent** は、Claude 3.5 Sonnet などの高性能な「メインAI」のトークン消費量とコストを劇的に削減するために設計された、Model Context Protocol (MCP) サーバーです。

コードの初稿作成、大規模なファイルの書き換え、技術コンテキストの翻訳など、最もトークンを消費する「泥臭い作業」を安価なサブLLM（Google Gemini Flash または ローカルの Ollama）に委譲します。メインAIは「指揮官（アーキテクト）」としての役割に専念させることができます。

## 🌟 主な機能

- **高度な実行パイプライン**:
    1. **翻訳フェーズ**: 日本語の指示やコンテキストを自動で英語に変換（チャンク分割対応）。トークン密度を最適化し、推論精度を向上させます。
    2. **圧縮フェーズ**: 参照コードがサブLLMの制限を超える場合、構造を維持したまま動的に要約。小型モデルでも動作可能にします。
    3. **下書きフェーズ**: 最適化された英語コンテキストを用いて、ピンポイントな差分またはコード全体を生成します。
- **動的なコンテキスト管理**: Gemini API や Ollama モデルの制限を自動で取得・推定し、実行前のオーバーフローを防止します。
- **マルチバックエンド対応**: `.env` の設定一つで、Google AI Studio (Gemini) とローカルホスト (Ollama) を自由に使い分け可能です。
- **強力なトレーサビリティ**: `Loguru` による構造化 JSON ログ、実行時間の計測、リクエストごとの `run_id` 付与により、ボトルネックを即座に特定。
- **安定した運用**: エラーのみを隔離する `error.log` や、致命的エラー時でもターミナルが勝手に閉じないガードロジックを搭載。

## 🏗️ 設計思想

本プロジェクトの根幹は **「意図的な思考コンテキストの遮断」** です。
- コードや要件といった「情報」はメインAIからサブエージェントへ徹底的に引き渡します。
- しかし、サブエージェントが返すのは **「実行結果（コード）」のみ** です。
- サブエージェントの推論プロセス（途中式）はあえて受け取らないことで、メインAIのコンテキストを清潔に保ち、高度な全体指揮に集中させます。

## 🚀 クイックスタート (Windows)

1.  **リポジトリのクローン**:
    ```bash
    git clone https://github.com/ayato-labs/Sub_cheap_McpAiAgent.git
    cd Sub_cheap_McpAiAgent
    ```

2.  **セットアップ**:
    自動セットアップスクリプトを実行します。`uv` を使用して仮想環境の作成と依存関係のインストールを行います。
    ```cmd
    setup.bat
    ```

3.  **環境変数の設定**:
    `.env.example` を参考に `.env` ファイルを作成し、APIキーを記入します。
    ```env
    GOOGLE_API_KEY=your_gemini_api_key
    TRANSLATION_MODEL=gemini-2.5-flash
    DRAFTING_MODEL=gemma2:9b
    ```

4.  **Claude Desktop への登録**:
    `claude_desktop_config.json` に以下の設定を追加します。
    ```json
    {
      "mcpServers": {
        "sub-cheap-mcp": {
          "command": "uv",
          "args": [
            "--directory",
            "C:/path/to/Sub_cheap_McpAiAgent",
            "run",
            "sub-cheap-mcp"
          ]
        }
      }
    }
    ```

5.  **起動**:
    ```cmd
    run.bat
    ```

## 🛠️ 詳細設定

モデルの切り替えや詳細な動作設定については、[docs/MCP_CONFIGURATION.md](docs/MCP_CONFIGURATION.md) を参照してください。

## 📄 意思決定記録 (ADR)

技術的な決定背景はすべてドキュメント化されています。
- [ADR-0001: サブLLMの選定戦略](docs/ADR/ADR-0001-selection-of-sub-llm-and-edit-strategy.md)
- [ADR-0004: Google AI Studio の採用](docs/ADR/ADR-0004-use-google-ai-studio-api.md)
- [ADR-0005: 専用翻訳モデル不採用の決定（KISS原則）](docs/ADR/ADR-0005-reject-dedicated-local-translation-models.md)
- [ADR-0006: Semgrep等を用いた内部QAループの不採用](docs/ADR/ADR-0006-reject-internal-qa-loops.md)
- [ADR-0007: MVPフェーズにおける自動タスクルーティングの不採用](docs/ADR/ADR-0007-reject-automated-task-routing-for-mvp.md)

## 🗺️ ロードマップと将来の展望

**現在のフェーズ (個人開発者向けMVP):**
現在、モデルのルーティングは `.env` ファイルによる明示的な指定に依存しています。これは、ユーザー自身がAPIキーを持ち込む「BYOK（Bring Your Own Key）」環境やローカル環境での実行を前提とした意図的な設計です。タスクの難易度を自動判定して高価なモデルへ勝手に切り替えたり、マシンのVRAMを超えるモデルをロードしたりする「自動タスクルーター」は導入していません。これにより、ユーザーはAPIコストとローカルリソースを100%制御し続けることができます。

**将来のSaaSフェーズ:**
マネージドなSaaSプラットフォームへと進化する際には、以下の実装を計画しています：
- **インテリジェント・タスクルーター**: プロンプトの複雑さを自動評価し、利益率とパフォーマンスを最大化するためにTier 1（Flash等）とTier 2（Pro/Opus等）のモデル間で自動ルーティングを行います。
- **自動QAリトライループ**: 静的解析（Semgrep等）に基づいてエラーを検知し、メインAIに結果を返す前にサブエージェント内部で自動修正ループを回します。

## 🏢 商用・ビジネス利用への対応 (Commercial & Business Use Ready)

本プロジェクトは、企業のビジネス環境やプロプライエタリなシステム内でも安全にご利用いただけるよう、コピーレフト型ライセンス（GPLなど）を排除し、寛容なオープンソースライセンス（Permissive License: MIT, Apache 2.0, BSD）の技術スタックのみで構築されています。

**依存ソフトウェア・ライセンス一覧:**
*   **[Ollama](https://github.com/ollama/ollama/blob/main/LICENSE)** (Local LLM Server): `MIT License`
*   **[FastMCP](https://github.com/jlowin/fastmcp/blob/main/LICENSE)** (MCP Framework): `MIT License`
*   **[google-genai](https://github.com/googleapis/python-genai/blob/main/LICENSE)** (Gemini SDK): `Apache License 2.0`
*   **[requests](https://github.com/psf/requests/blob/main/LICENSE)** (HTTP Client): `Apache License 2.0`
*   **[loguru](https://github.com/Delgan/loguru/blob/master/LICENSE)** (Logging): `MIT License`
*   **[python-dotenv](https://github.com/theskumar/python-dotenv/blob/main/LICENSE)** (Env Config): `BSD-3-Clause`

> **⚠️ 免責事項 (Important Disclaimer): AIモデル（重み）とAPI利用規約について**
> 本MCPサーバーおよび上記の依存ソフトウェアはすべて商用利用可能ですが、**バックエンドとして呼び出す「AIモデル（重みデータ）」や「APIサービス」のライセンスおよび利用規約は、各プロバイダーに依存します。**
> 例：Ollama経由で使用するローカルモデル（Gemma, Llama等）や、Google AI StudioのAPI規約については、お客様のビジネス要件（MAU上限、商用利用の可否など）に合致するか各自でご確認ください。

## ⚖️ ライセンス

MIT License. 詳細は [LICENSE](LICENSE) をご覧ください。
