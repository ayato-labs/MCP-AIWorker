# ADR-0003: Adoption of Pytest and Mocking Strategy

- **Date**: 2026-06-15
- **Status**: Accepted
- **Deciders**: Gemini CLI (Agent)

## Context
The project requires a robust testing framework to ensure a minimum of 80% coverage and to adhere to the rule of mocking external I/O boundaries. The initial setup only included a manual integration test script (`test_integration.py`), which is insufficient for automated CI/CD pipelines and costs money/tokens by directly calling LLM APIs during testing.

## Decision
1. **Adopt `pytest`**: Use `pytest` as the primary testing framework due to its simplicity, powerful fixture system, and ecosystem.
2. **Adopt `pytest-mock`**: Use `pytest-mock` to mock external API calls to Gemini and Ollama.
3. **Unit Test Focus**: Mock the `SubLLMClient` methods (`call_gemini`, `call_ollama`) to test the core logic (file reading/writing, line replacement, and input validation) without incurring API costs.

## Consequences
### Positive
- Fast, deterministic test execution without network dependency.
- Zero API costs during CI/CD runs.
- Easy integration into GitHub Actions.

### Negative / Risks
- Changes in the upstream LLM API responses (e.g., unexpected markdown formatting) won't be caught by unit tests since the API is mocked. Occasional manual integration tests are still required.

## References
- Issue: #1
- PR: # (TBD)
