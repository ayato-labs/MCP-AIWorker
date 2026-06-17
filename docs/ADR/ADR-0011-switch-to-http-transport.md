# ADR-0011: Switch from Stdio to Streamable HTTP Transport

- **Date**: 2026-06-17
- **Status**: Accepted
- **Deciders**: ayato-labs, Gemini Agent

## Context
Initially, the MCP server used the default Stdio transport. While Stdio is easy to set up for local desktop use, it creates a 1:1 binding between the client (e.g., Claude Desktop) and the server process. This prevents parallel tool execution from multiple AI agents or multiple threads within a single complex workflow, as only one process can own the pipe.

To support true parallelism and future-proof the system for a multi-agent or remote-access environment, we need a transport that allows multiple simultaneous connections.

## Decision
We will transition from Stdio to **Streamable HTTP**:
1. **Implementation**: Use FastMCP's capability to run as a Streamable HTTP server (transport="streamable-http").
2. **Connectivity**: The server will listen on a local port (default: 10300) and expose the `/mcp` endpoint.
3. **Execution**: A dedicated `run.bat` will be provided to launch the server as a background or independent process, decoupling it from the lifecycle of a single AI client.

## Consequences
### Positive
- **Parallelism**: Multiple AI agents can now call `sub-cheap-mcp` tools concurrently.
- **Improved Debugging**: HTTP requests can be inspected using standard network tools.
- **Modern Transport**: Streamable HTTP is the recommended modern transport for MCP, offering better performance and full-duplex capabilities over legacy SSE.


### Negative / Risks
- **Network Security**: Opening a port (even on localhost) increases the security surface. We must ensure it only listens on the intended interfaces.
- **Port Management**: Users must ensure the selected port is not occupied by other services.

## References
- MCP Specification: Server-Sent Events (SSE) Transport.
