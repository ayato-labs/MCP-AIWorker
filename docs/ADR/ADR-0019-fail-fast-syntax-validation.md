# ADR 0019: Fail-Fast Syntax Validation

## Status
Accepted

## Context
A significant bottleneck in the drafting process is the overhead of passing syntactically invalid code from the inexpensive Sub-LLM to the Architect or subsequent automated tests. This necessitates costly re-runs or manual intervention. We need a "Fail-Fast" mechanism to identify obvious syntax errors immediately after code generation.

## Decision
We implement a lightweight, static syntax validation step in the `draft_edit` pipeline that runs before the code is finalized/written to the filesystem. Additionally, we structure the error reporting from the Sub-LLM to Architect.

### Implementation Details
1.  **Language-Specific Validation**:
    - **Python**: Uses `ast.parse` to validate the code as a module or a wrapped code block (to handle snippets).
    - **Other Languages (PHP, C, etc.)**: Uses `subprocess` to invoke language-specific linting tools (e.g., `php -l`, `gcc -fsyntax-only`) if installed on the host.
2.  **Automated Repair**:
    - If a syntax error is detected, the `draft_edit` pipeline automatically constructs a repair prompt containing the error message and the original code, instructing the Sub-LLM to fix the syntax within a single retry attempt.
3.  **Structured Feedback Loop**:
    - Syntax validation now returns a JSON-structured object (`{"error_type": "...", "message": "...", "line": ...}`) instead of raw strings. This provides the Architect with specific, actionable metadata about the failure, minimizing re-inference overhead.
4.  **Graceful Fallback**:
    - If required CLI tools for non-Python languages are missing, the validation step skips the check rather than failing the process, ensuring compatibility across diverse environments.

## Consequences
### Positive
- **Latency Reduction**: Significantly reduces the number of times the Architect or the test suite encounters trivial `SyntaxError`s.
- **Cost Efficiency**: Reduces wasted tokens and API calls by catching errors before they propagate through the CI/CD pipeline.
- **Improved Reliability**: Provides an immediate feedback loop for the Sub-LLM to self-correct simple formatting or closure errors.

### Negative/Trade-offs
- **Host Dependency**: For non-Python languages, functionality relies on the presence of specific CLI tools on the host machine.
- **Complexity**: Slightly increases the complexity of the `draft_edit` pipeline logic.
