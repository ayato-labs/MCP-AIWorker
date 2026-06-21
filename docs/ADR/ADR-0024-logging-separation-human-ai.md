# ADR-0024: Separation of Human and Machine Logging

## Context
Our system uses a CLI-based architect-worker model. Initially, all logs were output as raw JSON to both the terminal and log files to ensure observability. This caused cognitive overload for the human developer (due to JSON verbosity) and made it difficult for the AI to parse useful information, as it had to filter through irrelevant console noise.

## Decision
We will explicitly separate logging streams by consumer:

1. **Terminal (Human Consumer):** Output will be simplified into a human-readable format (`HH:mm:ss | LEVEL | message`) using `loguru`. This focuses on task progress and high-level outcomes.
2. **Log Files (AI Consumer):** Output will remain JSON-serialized, comprehensive, and include debug-level information (`DEBUG+`), allowing AI agents to perform structured analysis, performance monitoring, and fault diagnosis without terminal interference.

## Consequences
- **Positive:** Terminal output is now clean and actionable for the developer. Automated agents have a reliable, machine-readable data source.
- **Negative:** Debugging requires opening a file rather than just looking at the terminal.
- **Maintenance:** The `logger.py` module now manages two distinct `loguru` handlers to maintain this separation.
