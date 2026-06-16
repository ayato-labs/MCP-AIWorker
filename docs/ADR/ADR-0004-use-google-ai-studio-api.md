# ADR-0004: Adoption of Google AI Studio API over Vertex AI

- **Date**: 2026-06-15
- **Status**: Accepted
- **Deciders**: ayato-labs (User), Gemini CLI (Agent)

## Context
When integrating Google Gemini models, there are two primary paths: Google AI Studio (Individual API Key based) and Vertex AI (Google Cloud Platform enterprise based). We need to decide which platform to standardize on for this project.

## Decision
Adopt **Google AI Studio API** for LLM integration.

## Rationale
1. **Low Overhead**: Google AI Studio allows for immediate setup with a simple API key. Vertex AI requires complex GCP project configuration, IAM roles, and potentially billing setups that are excessive for a "drafting surrogate" tool.
2. **Minimal Benefits of Sharing**: Shared infrastructure (Vertex AI) provides centralized management, which is a disadvantage here. The specific drafting tasks performed by this agent are better served by individual, isolated API keys.
3. **Reduced Complexity**: Sharing an environment increases friction in setup and introduces dependencies that do not exist with the AI Studio model.
4. **Cost Efficiency**: AI Studio offers a generous free tier for Gemini models, which directly aligns with the "Sub-cheap" goal of the project.

## Consequences
### Positive
- Extremely fast developer onboarding.
- No GCP project management required.
- Clear and simple environment variable configuration.

### Negative / Risks
- Lack of centralized logging or enterprise-grade security controls (though this is mitigated by the stateless nature of the sub-agent and the fallback to local Ollama).

## References
- [概念的要件定義書.md](../../docs/概念的要件定義書.md)
