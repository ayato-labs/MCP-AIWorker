# ADR-0022: Ignore Patterns for File Scanning to Improve Token Efficiency

## Status
Accepted

## Context
Tooling that performs repository-wide scans, such as `find_target` and repository map generation, was inadvertently scanning unnecessary directories like virtual environments (`.venv`), version control (`.git`), caches (`__pycache__`, `.pytest_cache`, `.ruff_cache`), and egg-info. This led to:
1. Excessive token consumption when feeding file structures to LLMs.
2. `400 INVALID_ARGUMENT` errors due to exceeding context window limits.
3. Slow execution times for file scanning operations.

## Decision
We will implement a mandatory ignore list for directory scanning operations. All tools within `mcp_ai_worker` that use `os.walk` or similar directory traversal techniques must filter out the following directories:
- `.venv`
- `.git`
- `__pycache__`
- `.pytest_cache`
- `.ruff_cache`
- `.egg-info`

## Consequences
- **Positive**: Significantly reduced context usage, improved tool performance, and resolution of context-limit-related errors.
- **Negative**: If a user genuinely needs to scan these directories, they will be unable to do so via these tools. This is considered acceptable for the scope of an AI assistant tool, as these directories rarely contain source code relevant to editing tasks.
