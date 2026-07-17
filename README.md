# ckg-nvidia-nemoclaw

**Model for language, graph for knowledge.** The NVIDIA NemoClaw stack as a traversable knowledge graph — MCP-native, deterministic, 11× fewer tokens than RAG.

55 nodes · 74 edges · covers the full NemoClaw ecosystem: OpenShell runtime, OpenClaw, Hermes, LangChain Deep Agents, inference routing, network policy, security architecture, progressive tool disclosure, managed MCP servers, FOX Blueprint, and the Nemotron 3 Ultra agent harness.

> *The graph doesn't guess — it traverses. Every answer traces to a declared edge.*

## Why this exists

Agents building on NemoClaw burn tokens reconstructing relationships that are already declared in the docs. This package pre-structures those relationships as a typed dependency graph. Instead of retrieving docs, the model traverses declared edges.

**Local A/B test (CPU-only, Ollama, same harness):**

| Model | Bare F1 | + CKG F1 | Lift |
|-------|---------|----------|------|
| phi4-mini (2.5 GB) | 0.047 | 0.325 | **+598%** |
| nemotron-mini (4B) | 0.174 | 0.412 | **+137%** |

phi4-mini + CKG outperforms nemotron-mini bare by 86%. A laptop model with a graph beats a specialized model without one.

## Use as a claude.ai connector (remote)

Add this URL in claude.ai → Settings → Connectors:

```
https://ckg-nvidia-nemoclaw.onrender.com/mcp
```

## Use locally (Claude Desktop / Claude Code)

```bash
pip install ckg-nvidia-nemoclaw
# or
uvx ckg-nvidia-nemoclaw
```

Claude Desktop config:

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
| `ask_nemoclaw(question)` | Natural language query — auto-detects and traverses the relevant subgraph |
| `query_ckg(concept, depth)` | Typed subgraph around a specific concept (1–5 hops) |
| `get_prerequisites(concept)` | Full upstream prerequisite chain |
| `search_concepts(query)` | Fuzzy search across all 55 concepts |
| `list_domains()` | Available domains and node/edge counts |

## Coverage

- **Agent runtimes:** OpenClaw · Hermes (Nous Research) · LangChain Deep Agents Code
- **Platform:** OpenShell · NVIDIA Agent Toolkit · CONNECT proxy · L7 proxy · Landlock LSM
- **Inference:** inference.local routing · SharedGateway · vLLM · Ollama · Local NIM · ModelRouter
- **Policy:** NetworkPolicy · PolicyTier (Restricted/Balanced/Open) · PolicyPreset bundles
- **Security:** 5-layer architecture (Network/Filesystem/Process/Gateway Auth/Inference)
- **Features:** Progressive Tool Disclosure · Context Compaction · Managed MCP Servers · Snapshots · Shields
- **Deployment:** Local CLI · Brev CLI · Brev Web UI · DGX Spark · macOS Apple Silicon · WSL2
- **Ecosystem:** FOX Blueprint · MoMClaw (Foxconn) · Nemotron 3 Ultra · Agent Harness ecosystem

## Benchmark (v0.6.2 locked)

| System | Macro F1 | Mean tokens | Cost / 1k queries |
|--------|----------|-------------|-------------------|
| CKG | **0.471** | 269 | $7.81 |
| RAG | 0.123 | 2,982 | $76.23 |
| GraphRAG | 0.120 | ~3,000 | ~$76 |

[Full paper](https://github.com/Yarmoluk/ckg-benchmark/blob/main/paper/main.pdf)

---

Built by [Graphify.md](https://graphifymd.com) · [PyPI](https://pypi.org/project/ckg-nvidia-nemoclaw/) · patent pending
