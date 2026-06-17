@echo off
setlocal
cd /d "%~dp0"

if not exist .venv (
    echo Error: .venv directory not found. Please run setup.bat first.
    pause
    exit /b 1
)

echo Starting Sub-cheap-McpAiAgent (Transport: SSE)...
:: Default to sse for parallel support. To use stdio: run.bat stdio
set TRANSPORT=sse
if "%~1" neq "" set TRANSPORT=%~1

uv run mcp_server.py %TRANSPORT%
if %errorlevel% neq 0 (
    echo Server exited with error code %errorlevel%.
    pause
)
