# ADR-0023: Token Observatory for Cost Optimization

## Status
Implemented

## Context
As part of the MCP-AIWorker Long-Term Development Plan, a core objective is to quantitatively prove the cost efficiency of the system. Without reliable, automated metrics of token consumption, it is impossible to validate the effectiveness of our context compression and Architect-Worker delegation strategies.

## Decision
We have implemented a "Token Observatory" system to track and store token consumption metrics. Key architectural decisions include:

1.  **Instrumentation Strategy**: Used a Python decorator (`@track_metrics`) applied to all MCP tools (`@mcp.tool()`) to automatically wrap and measure execution time and token usage.
2.  **Storage**: Utilized a local SQLite database (`metrics.db`) for lightweight, persistent storage of metrics.
3.  **Data Flow**:
    *   `metrics.py` manages database interaction and context-aware tracking.
    *   `SubLLMClient` (in `client.py`) is updated to record token usage via `log_token_usage` whenever an LLM API call is made.
    *   `logger.py` acts as the bridge to pass token data from the LLM client to the active tracking context.
4.  **CLI Dashboard**: Provided `scripts/show_dashboard.py` to allow users to instantly visualize total token consumption and estimated costs based on pre-defined provider pricing models.

## Consequences
- **Positive**:
    - Quantitative validation of the core "cost optimization" mission.
    - Enables future automated cost benchmarking (Phase 7).
    - Provides transparency into how different tasks impact API costs.
- **Negative/Risk**:
    - Minimal added overhead due to database writes per tool execution.
    - Requires maintenance of pricing data in the dashboard script as API models change.
