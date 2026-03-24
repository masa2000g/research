# Technical Research: Model Context Protocol (MCP)

## Overview

MCP is an open standard introduced by Anthropic in November 2024 that defines how AI systems (LLMs, agents) connect to external tools and data sources. It solves the "N×M integration problem": before MCP, connecting N tools with M model front-ends required N×M custom adapters. MCP collapses this to N+M by providing a single shared protocol layer.

The closest analogy is the **Language Server Protocol (LSP)**, which standardized how IDEs communicate with language analyzers. MCP applies the same idea to AI agents and external capabilities.

## Key Findings

1. **Client-server architecture over JSON-RPC 2.0** — all communication is stateful and bidirectional via JSON-RPC sessions.
2. **Three server-side primitives** — Tools, Resources, and Prompts form the complete capability surface exposed by any MCP server.
3. **Two transport modes** — stdio (local processes) and Streamable HTTP (network deployments); the latter is the focus of the 2026 scalability roadmap.
4. **OAuth 2.1 security layer** — MCP servers are now formally classified as OAuth Resource Servers; auth hardening is ongoing.
5. **SDKs in Python, TypeScript, C#, Java** — lowering the barrier for server authors.

## Detailed Analysis

### Architecture

MCP separates responsibilities into four roles:

| Role | Description |
|------|-------------|
| **Host** | The application (e.g., Claude Desktop, an IDE) that orchestrates sessions |
| **Client** | A per-session component inside the Host that manages one MCP connection |
| **Server** | A lightweight process exposing capabilities from a data source or service |
| **Data Source** | The actual backend: filesystem, database, external API, etc. |

A Host spawns multiple isolated Client sessions simultaneously, each connecting to a separate Server. Sessions are stateful JSON-RPC channels, meaning context is preserved across multiple round-trips.

### Core Primitives

**Server-side primitives** (what a server offers to the host):

| Primitive | Purpose |
|-----------|---------|
| **Tools** | Callable functions — e.g., `create_github_issue`, `query_database` |
| **Resources** | Structured data the AI can read — files, records, API responses |
| **Prompts** | Reusable prompt templates with parameterized inputs |

**Client-side primitives** (what a client exposes back to the server):

| Primitive | Purpose |
|-----------|---------|
| **Roots** | Filesystem root hints so the server knows what paths to trust |
| **Sampling** | Allows a server to request an LLM completion from the host |
| **Elicitation** | Allows a server to ask the user a question through the host UI |

The bidirectional nature (servers can also call back to the host) is what distinguishes MCP from simpler function-calling APIs.

### Transport & Communication

- **stdio transport**: Server runs as a child process; communication is via stdin/stdout. Ideal for local tools.
- **Streamable HTTP**: Server runs as an HTTP service; supports server-sent events for streaming. Required for cloud deployments.

The November 2025 spec update focused heavily on making Streamable HTTP production-ready. The 2026 roadmap addresses horizontal scaling, load balancer compatibility, and stateless session resumption.

### Security Model

As of June 2025, MCP servers are formally OAuth Resource Servers. Key additions:
- Protected Resource Metadata endpoints (`.well-known` discovery)
- Client Identifier Metadata Documents (CIMD) to prevent token theft by malicious servers
- DPoP (Demonstration of Proof-of-Possession) tokens on the 2026 roadmap
- Workload Identity Federation for server-to-server auth

A 2025 security audit found that nearly all publicly accessible MCP servers lacked authentication, highlighting a gap between protocol capability and real-world deployment practices.

### MCP Server Cards

Planned for 2026: a `.well-known/mcp-server` endpoint where servers expose structured metadata (capabilities, auth requirements, rate limits) without requiring a client connection. This enables automated discovery and registry indexing.

## Data and Evidence

| Metric | Value | Source |
|--------|-------|--------|
| Monthly SDK downloads | 97M+ (by Nov 2025) | [MCP Blog](http://blog.modelcontextprotocol.io/posts/2025-11-25-first-mcp-anniversary/) |
| Available MCP servers (Sept 2025) | ~2,000 in registry | [Model Context Protocol Blog](http://blog.modelcontextprotocol.io/posts/2025-11-25-first-mcp-anniversary/) |
| Registry growth in one month | 407% | Search result |
| SDKs supported | Python, TypeScript, C#, Java | [MCP Spec](https://modelcontextprotocol.io/specification/2025-11-25) |
| Current spec version | 2025-11-25 | [Spec](https://modelcontextprotocol.io/specification/2025-11-25) |

## Uncertainty and Limitations

- **Security immaturity**: The protocol's auth model is still stabilizing; enterprise deployments require careful hardening beyond what the base spec mandates.
- **Stateful sessions at scale**: Running MCP at scale behind load balancers is an unsolved problem being addressed in the 2026 roadmap.
- **Agent-to-Agent semantics**: The spec currently handles Host→Server communication; A2A (Agent-to-Agent) is experimental and not yet standardized.
- **Discovery fragmentation**: Without universal MCP Server Cards adoption, finding and evaluating servers remains ad hoc.

## Sources

- [MCP Specification 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25)
- [One Year of MCP — Model Context Protocol Blog](http://blog.modelcontextprotocol.io/posts/2025-11-25-first-mcp-anniversary/)
- [MCP Spec Updates June 2025 (Auth)](https://auth0.com/blog/mcp-specs-update-all-about-auth/)
- [Model Context Protocol — Wikipedia](https://en.wikipedia.org/wiki/Model_Context_Protocol)
- [MCP Technical Overview — CodiLime](https://codilime.com/blog/model-context-protocol-explained/)
- [MCP Introduction — Stytch](https://stytch.com/blog/model-context-protocol-introduction/)
