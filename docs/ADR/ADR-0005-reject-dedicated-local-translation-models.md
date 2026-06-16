# ADR-0005: Rejection of Dedicated Local Translation Models

- **Date**: 2026-06-15
- **Status**: Accepted
- **Deciders**: ayato-labs (User), Gemini CLI (Agent)

## Context
As part of the multi-stage pipeline (Translation -> Compression -> Drafting), we evaluated whether to use dedicated, lightweight, permissive-licensed local Machine Translation (MT) models (e.g., Argos Translate, Opus-MT) for the translation phase instead of relying on the sub-LLM (e.g., Gemini Flash). The goal was to potentially save token costs and reduce reliance on LLMs for simple translation tasks.

## Decision
**Reject** the integration of dedicated local MT models. The system will continue to use the sub-LLM (configured via `TRANSLATION_MODEL` in `.env`) for the translation phase.

## Rationale
1. **Architectural Simplicity (KISS)**: Introducing dedicated MT models requires adding heavy dependencies (hundreds of megabytes of weights, C++ inference engines like CTranslate2). This destroys the core value proposition of the project: being a highly portable, single-file MCP server (`mcp_server.py`).
2. **Uniform Interface**: By using the sub-LLM for translation, compression, and drafting, all operations route through a single, clean interface (`SubLLMClient.call_any`).
3. **Code-Aware Translation**: Legacy MT models often struggle with preserving programming syntax (variable names, indentation, code blocks) during translation. LLMs are significantly better at understanding instructions like "Translate this while preserving code structure."
4. **False Economy**: The cost of using inexpensive LLMs (like Gemini Flash free tier or local Ollama) for translation is negligible. The effort to manage, maintain, and containerize a separate ML translation pipeline far outweighs the token savings.

## Consequences
### Positive
- The codebase remains clean, lightweight, and free of massive binary dependencies.
- Setup remains simple (`uv pip install -e .`) without requiring users to manually download model weights.
- High translation quality that preserves coding contexts.

### Negative / Risks
- Relies on the availability and token limits of the configured `TRANSLATION_MODEL` (mitigated by the generous free tiers and local Ollama fallback).

## References
- Issue: #5
- PR: #6
