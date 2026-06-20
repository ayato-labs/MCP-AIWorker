# ADR-0015: Structured Logging with Loguru

- **Date**: 2026-06-20
- **Status**: Accepted
- **Deciders**: ayato-labs, Antigravity Agent

## Context
As the `MCP-AIWorker` expanded in complexity, identifying and debugging failures in the asynchronous pipeline (Translation -> Target Inference -> Snippet Extraction -> Drafting -> Writeback) became difficult. Standard `print` statements lacked the necessary metadata (timestamps, log levels, run IDs, stack traces) and were not persisted across executions, making it impossible to perform post-mortem analysis of failures occurring in the production environment.

## Decision
We implemented a structured logging system using the `loguru` library to enhance observability and traceability.

1. **Centralized Logger Configuration**:
   - Created `mcp_ai_worker/logger.py` to centralize all logging logic.
   - Configured **Structured JSON Logging** for both console (stderr) and file outputs to enable easy integration with log analysis tools.
   - Enabled `backtrace=True` and `diagnose=True` to capture detailed exception information.

2. **Log Persistence and Retention**:
   - Implemented a per-execution log file strategy: each run creates a new file named `logs/execution_{timestamp}.log`.
   - Added a retention policy that automatically deletes older logs, keeping only the **two most recent execution files** to prevent disk space exhaustion.

3. **Integration across Modules**:
   - Replaced `print` and basic `logging` calls with `logger.debug`, `logger.info`, `logger.warning`, and `logger.error` in `server.py`, `client.py`, and `utils.py`.
   - Integrated `logger.exception()` within `try...except` blocks to capture full stack traces for fatal errors.

## Consequences
### Positive
- **Enhanced Debugging**: JSON logs provide structured metadata (time, level, module, line number) that allows for precise error localization.
- **Traceability**: The use of `logger.contextualize(run_id=...)` (already present in some tools) now maps directly to structured log records, enabling the correlation of events within a single request.
- **Automated Maintenance**: The retention policy ensures that logs do not grow indefinitely while still providing enough history for the most recent failures.

### Negative / Risks
- **Dependency**: Introduces `loguru` as a mandatory dependency.
- **Log Volume**: `DEBUG` level logging in JSON format can generate large files quickly if the system is under heavy load.

## References
- [Loguru Documentation](https://github.com/Delgan/loguru)
