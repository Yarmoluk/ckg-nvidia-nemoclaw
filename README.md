# ckg-nvidia-nemoclaw

NVIDIA NemoClaw as a traversable knowledge graph — MCP-native.

**55 nodes · 74 edges** covering the full NemoClaw stack: OpenShell runtime, OpenClaw, Hermes, LangChain Deep Agents, inference routing, network policy, security architecture (L7 proxy, Landlock LSM, CONNECT proxy), progressive tool disclosure, managed MCP servers, deployment paths (local, Brev), FOX Blueprint, and the Nemotron 3 Ultra agent harness ecosystem.

Instead of retrieving docs, the agent traverses declared typed relationships. Every answer traces to a declared edge — the graph doesn't guess, it traverses.

**Benchmark (KRB v0.6.2 locked):** CKG F1 0.471 · RAG baseline 0.123 · GraphRAG baseline 0.120 · 269 tokens/query vs 2,982 (11× reduction)

## Install

```bash
pip install ckg-nvidia-nemoclaw
```

## Run as MCP Server

```bash
uvx ckg-nvidia-nemoclaw
```

## Claude Desktop Config

```json
{
  "mcpServers": {
    "nemoclaw": {
      "command": "uvx",
      "args": ["ckg-nvidia-nemoclaw"]
    }
  }
}
```

## Tools

| Tool | Description |
|------|-------------|
| `ask_nemoclaw(question)` | Auto-detect and traverse the relevant subgraph |
| `query_ckg(concept, depth)` | Typed subgraph around a specific concept |
| `get_prerequisites(concept)` | Full upstream prerequisite chain |
| `search_concepts(query)` | Fuzzy search concepts by name or keyword |
| `list_domains()` | List available domains and node/edge counts |

## Coverage

- **Agent runtimes:** OpenClaw · Hermes (Nous Research) · LangChain Deep Agents Code
- **Platform:** OpenShell · NVIDIA Agent Toolkit · CONNECT proxy · L7 proxy · Landlock LSM
- **Inference:** inference.local routing · SharedGateway · vLLM · Ollama · Local NIM · ModelRouter
- **Policy:** NetworkPolicy · PolicyTier (Restricted/Balanced/Open) · PolicyPreset bundles
- **Security:** 5-layer architecture (Network/Filesystem/Process/Gateway Auth/Inference)
- **Features:** Progressive Tool Disclosure · Context Compaction · Managed MCP Servers · Snapshots · Shields
- **Deployment:** Local CLI · Brev CLI · Brev Web UI · DGX Spark · macOS Apple Silicon · WSL2
- **Ecosystem:** FOX Blueprint · MoMClaw (Foxconn) · Nemotron 3 Ultra · Agent Harness ecosystem

## Benchmark

[github.com/Yarmoluk/ckg-benchmark/blob/main/paper/main.pdf](https://github.com/Yarmoluk/ckg-benchmark/blob/main/paper/main.pdf)

---

Built by [Graphify.md](https://graphifymd.com) · patent pending
