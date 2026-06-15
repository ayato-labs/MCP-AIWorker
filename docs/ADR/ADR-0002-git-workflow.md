# ADR-0002: Git Workflow and Branch Protection

- **Date**: 2026-06-15
- **Status**: Accepted
- **Deciders**: Gemini CLI (Agent)

## Context
Standardizing the development workflow is crucial for collaboration and code quality. We need a way to ensure that changes are reviewed and that the main branches are protected from accidental direct pushes or deletions.

## Decision
1.  **Branching Strategy**: Adopt a simplified Git Flow.
    - `main`: Production-ready code.
    - `develop`: Integration branch for features.
    - Feature branches: Created from `develop` for specific tasks.
2.  **Branch Protection**:
    - Enable GitHub Repository Rulesets for `main` and `develop`.
    - Require at least 1 approving review for Pull Requests.
    - Restrict deletions and non-fast-forward pushes.
3.  **Bypass Actor**: Allow `ayato-labs` to bypass these rules for emergency fixes and repository management.

## Consequences
### Positive
- Increased code quality through mandatory PR reviews.
- Protection against accidental data loss or history overwrites.
- Clear separation between stable and development states.

### Negative / Risks
- Slight overhead in development velocity due to PR requirements.

## References
- [GEMINI.md](../../.gemini/GEMINI.md) (Git rules section)
- GitHub Ruleset ID: 17693730
