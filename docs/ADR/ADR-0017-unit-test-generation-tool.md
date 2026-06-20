# ADR 0017: Unit Test Generation Tool

## Status
Accepted

## Context
Inconsistent test quality from inexpensive Sub-LLMs is a known challenge. To improve this, we need a mechanism that enforces best practices (AAA Pattern), ensures comprehensive coverage (Test Matrix), and structures the Sub-LLM's reasoning process (Chain of Thought) when generating unit tests.

## Decision
We implement a dedicated MCP tool `generate_unit_tests` that utilizes an Architect-Worker delegation model, emphasizing pre-analysis by the Architect and strict framework enforcement for the Sub-LLM.

### Implementation Details
1. **Architect-Enforced Specification**:
   - The Main AI (Architect) is responsible for analyzing the source file and injecting specific edge cases/test matrix requirements via the `additional_instruction` parameter.
2. **Framework Enforcement (CoT)**:
   - Use an externalized system prompt (`prompts/unit_test_system_prompt.txt`) to enforce:
     - **AAA Pattern**: Explicit Arrange, Act, Assert blocks in comments.
     - **Isolation**: Mocking all external dependencies.
     - **CoT Structure**: Forcing the Sub-LLM to output a `<test_plan>` XML block before generating the actual code in a `<draft_output>` XML block.
3. **Pipeline**:
   - The server parses these XML blocks to validate the plan and extract the final code reliably, even if the stream is truncated or noisy.

## Consequences
### Positive
- **Improved Test Quality**: AAA pattern and CoT structure significantly reduce hallucinations and improve the robustness of generated tests.
- **Maintainability**: Clear test plans allow the Architect to quickly verify the Sub-LLM's intent.
- **Architectural Alignment**: Fits perfectly into the established Architect-Worker delegation model.

### Negative/Trade-offs
- **Scope Limitation**: Intentionally restricted to isolated unit tests (no integration tests), requiring the Architect to understand this boundary.
- **Sub-LLM Capability**: Relies on the Sub-LLM's ability to follow complex prompting instructions; if it fails, it increases the Architect's overhead to refine the prompt.
