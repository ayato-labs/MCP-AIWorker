# AGENTS.md - MCP-AIWorker

## Developer Commands

- **Setup**: `setup.bat` (Uses `uv` to create `.venv` and install dependencies).
- **Run Server**: `run.bat` (Starts server on `http://127.0.0.1:10300/mcp`).
- **Test**: `.venv\Scripts\python.exe -m pytest tests/integration/`
- **Lint**: `.venv\Scripts\python.exe -m ruff check .`
- **Order**: `Lint -> Test`

## Architecture & Entrypoints

- **Paradigm**: Architect-Worker model. The main AI (Architect) delegates mechanical tasks (drafting, translation, summarization) to sub-LLMs (Workers) via MCP tools.
- **Transport**: Streamable HTTP (SSE) on port 10300.
- **Main Entrypoint**: `mcp_server.py`
- **Core Logic**: `mcp_ai_worker/server.py` (Tool implementations) and `mcp_ai_worker/utils.py` (Helper functions).
- **Prompts**: Externalized in `prompts/*.txt`.

## Tooling Constraints

- **Absolute Paths**: All file-based tools (`draft_code`, `find_and_draft_edit`) **require absolute paths**.
- **`draft_code`**: Can create new files and directories automatically.
- **`find_and_draft_edit`**: Uses `grep-ast` for repository-wide targeting.
- **`execute_command`**: Summarizes long logs using a sub-LLM to save context tokens.
- **`fetch_and_summarize_url`**: Does not support Single Page Applications (SPAs).

## Environment & Setup

- **Python**: `3.10+`
- **Config**: Environment variables are loaded from `.env`.
- **Dependencies**: Uses `uv` for fast dependency management.
