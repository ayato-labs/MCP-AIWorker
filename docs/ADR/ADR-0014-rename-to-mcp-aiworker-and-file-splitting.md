# ADR-0014: Rename to MCP-AIWorker and Modular File Splitting

- **Date**: 2026-06-20
- **Status**: Accepted
- **Deciders**: ayato-labs, Antigravity Agent

## Context
As the project evolved, two major architectural and branding issues became apparent:
1. **Monolithic Codebase**: The core server code in `server.py` grew to over 700 lines. It mixed FastMCP server startup/tool declarations, sub-LLM provider client logic (Gemini, Ollama, Genspark), and complex text/regex utilities. This coupled structure violated the Single Responsibility Principle and made unit testing difficult.
2. **Branding and Identity**: The original name `Sub-cheap-McpAiAgent` used the word "cheap," which created a connotation of budget or low-quality code generation. It also failed to reflect the "Architect-Worker" paradigm (where high-performance frontier models like Claude 5 act as the architect and delegate sub-tasks to workers). 

To improve codebase maintainability and align branding with modern LLM standards (e.g. Claude 5 / Fable 5), we needed to refactor the project file structure and rename the package and repository.

## Decision
We implemented the following changes:
1. **Project Renaming**: Rebranded the repository name to `MCP-AIWorker` and renamed the internal Python package directory to `mcp_ai_worker`.
2. **Modular File Splitting**: Split `server.py` into three decoupled modules:
   - [client.py](file:///c:/Users/saiha/My_Service/programing/MCP/Sub_cheap_McpAiAgent/mcp_ai_worker/client.py): Contains all LLM communication logic and model client classes (`SubLLMClient`).
   - [utils.py](file:///c:/Users/saiha/My_Service/programing/MCP/Sub_cheap_McpAiAgent/mcp_ai_worker/utils.py): Holds pure utility functions for code parsing, XML extraction, text translation, repository mapping, and file reads/writes.
   - [server.py](file:///c:/Users/saiha/My_Service/programing/MCP/Sub_cheap_McpAiAgent/mcp_ai_worker/server.py): Contains only the FastMCP instance, tool route declarations, and the entry point `main()`.
3. **Backward Compatibility**: Configured `server.py` to import and re-export core classes (such as `SubLLMClient` and `draft_code`) to ensure existing test suites and third-party callers do not break.
4. **Documentation Refresh**: Updated both English and Japanese README documents to use the new naming scheme and updated LLM references to point to Claude 5 (Fable 5) as the primary frontier model.

## Consequences
### Positive
- **Improved Code Maintainability**: Splitting client, utility, and routing concerns dramatically decreases file complexity and aligns with SRP.
- **Enhanced Testability**: Moving text extraction and clean up helpers to `utils.py` allows testing them in isolation without bootstrapping the FastMCP server or initializing client APIs.
- **Polished Brand Identity**: The name `MCP-AIWorker` focuses on the "Worker" delegation paradigm, which sounds cleaner, more professional, and easier to search.

### Negative / Risks
- **Local Settings / Registry Updates**: Users will need to manually rename their registration configurations in `claude_desktop_config.json` from `sub-cheap-mcp` to `mcp-ai-worker`.
- **Manual Repository Rename**: The GitHub remote URL must be updated manually via the GitHub Web UI or CLI because rename settings are not exposed through the standard GitHub MCP server tools.

## References
- [ADR-0010: Embrace "Draft Quality" and Architect-Part-timer Division of Labor](file:///c:/Users/saiha/My_Service/programing/MCP/Sub_cheap_McpAiAgent/docs/ADR/ADR-0010-architect-parttimer-delegation-model.md)
- [ADR-0011: Switch from Stdio to Streamable HTTP Transport](file:///c:/Users/saiha/My_Service/programing/MCP/Sub_cheap_McpAiAgent/docs/ADR/ADR-0011-switch-to-http-transport.md)
