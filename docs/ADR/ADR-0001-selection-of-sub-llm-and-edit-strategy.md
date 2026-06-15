# ADR-0001: Selection of Sub-LLM and Pinpoint Edit Strategy

- **Date**: 2026-06-15
- **Status**: Accepted
- **Deciders**: Gemini CLI (Agent)

## Context
The primary goal of this project is to minimize token consumption for high-performance "Main AI" models. Large file reads and writes are the most significant contributors to token costs. We need an inexpensive but capable "Sub-LLM" to handle the "drafting" and "dirty work" of file modification.

## Decision
1.  **Sub-LLM Selection**: Use `gemma-4-31b-it` (available via Google AI Studio's free tier). 
    - **Reasoning**: It is a state-of-the-art open model with high performance-to-cost ratio (free tier support), and it is capable of following complex code modification instructions.
2.  **Pinpoint Edit Strategy**: Instead of sending the full file to the sub-LLM, only send a specific line range (`start_line` to `end_line`) plus minimal context.
    - **Reasoning**: This reduces the "round-trip" tokens for both the main AI (which only sends instructions and small snippets) and the sub-LLM.

## Consequences
### Positive
- Drastic reduction in token costs for the Main AI.
- Faster response times for large files as only snippets are processed.
- Fallback capability to local Ollama ensures availability even with API limits.

### Negative / Risks
- **Context Loss**: The sub-LLM might lack awareness of the full file structure, potentially leading to import errors or inconsistent naming.
- **Dependency**: Reliance on Google AI Studio's availability and specific model identifiers.

## References
- [概念的要件定義書.md](../../docs/概念的要件定義書.md)
- Issue: #1 (Initial Implementation)
