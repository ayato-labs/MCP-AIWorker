# ADR-0020: AST-Based Semantic Context Compression

Date: 2026-06-20
Status: Accepted

## Context
The previous context compression mechanism relied solely on LLM-based summarization. This often led to loss of critical information such as class interfaces, function signatures, and type definitions, which are essential for Sub-LLMs to generate accurate code.

## Decision
Implement an AST-based semantic compression mechanism. 
- Use Python's built-in `ast` module to parse Python code.
- Automatically replace the bodies of functions and methods with `...` (ellipsis), while preserving structural definitions (class/function signatures, typing).
- Pre-process all reference context with this AST compressor before passing it to the LLM-based compressor.

## Consequences
- **Pros**:
  - Significantly reduces token consumption while retaining essential structural context.
  - Improves code generation accuracy for inexpensive models by ensuring they have the necessary interface definitions.
  - Zero added external dependencies (uses standard `ast` library).
- **Cons**:
  - Only supports Python code parsing via `ast`.
  - Might still lose logic if `...` replacement is too aggressive in specific edge cases.
