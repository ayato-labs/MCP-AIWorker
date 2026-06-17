# MCP Configuration Guide

This guide explains how to configure and use the **Sub-cheap-McpAiAgent** server with your AI client (e.g., Claude Desktop).

## 1. Prerequisites
- **Python 3.10+**
- **uv**: The recommended package manager for this project.
- **Google AI Studio API Key**: For Gemini access. [Get one here](https://aistudio.google.com/app/apikey).
- **Ollama (Optional)**: For local LLM support.

## 2. Environment Variables (.env)
Create a `.env` file in the project root with the following settings. The system uses a multi-phase LLM approach to optimize tokens:

```env
# Google AI Studio
GOOGLE_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.5-flash

# Ollama (Local)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=gemma2:9b

# Role-based Model Selection ('gemini' or 'ollama')
TRANSLATION_MODEL=gemini  # Used for translating Japanese to English and chunking
DRAFTING_MODEL=gemini     # Used for context compression and actual code drafting
```

## 3. Claude Desktop Configuration
Since we have switched to **Streamable HTTP (SSE)** to support parallel agent execution, you must run the server independently.

### Step 1: Start the Server
Run the provided `run.bat` in the project root. This will start the MCP server on `http://localhost:8000`. Keep this window open.

### Step 2: Register in Claude Desktop
Add the following to your `claude_desktop_config.json` (located at `%APPDATA%\Claude\claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "sub-cheap-mcp": {
      "url": "http://localhost:8000/sse"
    }
  }
}
```
*Note: If you need to use the old Stdio mode (not recommended for parallel use), you can run `run.bat stdio` and use the previous `command`/`args` configuration.*


## 4. Usage Philosophy: Architect vs. Part-timer
This tool follows a specific delegation model:
- **Architect (Main AI)**: Responsible for high-level reasoning, gathering context, and performing final QA/integration.
- **Part-timer (Sub-LLM)**: Responsible for the tedious "heavy lifting" of typing code snippets or drafting files.

### Guidelines for the Architect (Main AI)
1. **Delegate Early**: Use `draft_code` to generate the bulk of your code changes to save your own context tokens.
2. **Accept "Draft" Quality (叩き台)**: The output is a draft. It may contain minor logical gaps or missing imports. This is an intentional tradeoff for speed and cost.
3. **Review & Refine**: After the tool returns, you **MUST** read the generated code and refine it to ensure it perfectly integrates with the existing system.

### Example Tool Call
The Main AI (Claude) will call the tool as follows:
- **path**: `src/main.py`
- **instruction**: `Add a docstring and implement the validate_input method with basic regex.`
- **start_line**: 20
- **end_line**: 35
- **reference_context**: (Optional snippets of related classes/utilities)

## 5. Traceability & Logs
- **mcp_server.log**: Contains structured JSON logs of the last 2 runs.
- **error.log**: Dedicated log file for error isolation.
- **run_id**: Each request is tagged with a unique UUID for easy tracking.
