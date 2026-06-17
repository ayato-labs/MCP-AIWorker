@echo off
setlocal
cd /d "%~dp0"

if not exist .venv (
    echo Error: .venv directory not found. Please run setup.bat first.
    pause
    exit /b 1
)

echo Starting Sub-cheap-McpAiAgent (Transport: Streamable HTTP)...

:: Use python directly from venv to avoid locking issues
.venv\Scripts\python.exe mcp_server.py
if %errorlevel% neq 0 (
    echo.
    echo Server exited with error code %errorlevel%.
    pause
)
