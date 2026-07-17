<!-- mcp-name: io.github.Yarmoluk/ckg-nvidia-nemoclaw -->

<div align="center">

# ckg-nvidia-nemoclaw

### NVIDIA NemoClaw as a traversable knowledge graph — MCP-native

**Your agents hallucinate NemoClaw's architecture. This graph declares it.**

[![PyPI version](https://img.shields.io/pypi/v/ckg-nvidia-nemoclaw?color=0f6e56&label=PyPI)](https://pypi.org/project/ckg-nvidia-nemoclaw/)
[![Python](https://img.shields.io/pypi/pyversions/ckg-nvidia-nemoclaw?color=0f6e56)](https://pypi.org/project/ckg-nvidia-nemoclaw/)
[![License: MIT](https://img.shields.io/badge/license-MIT-0f6e56)](LICENSE)
[![F1: 0.471 · 4× RAG](https://img.shields.io/badge/F1-0.471_%C2%B74%C3%97_RAG-0f6e56)](https://github.com/Yarmoluk/ckg-benchmark/blob/main/paper/main.pdf)
[![KRB v0.6.2](https://img.shields.io/badge/benchmark-KRB_v0.6.2-13201c)](https://github.com/Yarmoluk/ckg-benchmark/blob/main/paper/main.pdf)
[![Built by Graphify.md](https://img.shields.io/badge/built_by-Graphify.md-0f6e56)](https://graphifymd.com)

> *The graph doesn't guess — it traverses. Every answer traces to a declared edge.*

[**PyPI →**](https://pypi.org/project/ckg-nvidia-nemoclaw/) · [**Benchmark →**](https://github.com/Yarmoluk/ckg-benchmark/blob/main/paper/main.pdf) · [**graphifymd.com →**](https://graphifymd.com)

</div>

---

## The problem with NemoClaw context

NemoClaw's architecture spans eight layers — OpenShell platform, three agent runtimes (OpenClaw, Hermes, LangChain Deep Agents), inference routing, network policy, security hardening, and the FOX Blueprint ecosystem. The relationships between them are non-obvious and deep.

Agents reasoning about NemoClaw without structured context do one of three things:

| Approach | What breaks |
|---|---|
| Raw docs in context | 3,000+ tokens per query. No traversal. Drifts with model version. |
| RAG retrieval | Probabilistic. Accuracy degrades at each hop. Misses prerequisite chains. |
| Asking the model | Confident hallucinations about deployment paths that don't exist. |

All three share the same failure: the agent **re-infers** NemoClaw's architecture on every query instead of reading relationships that were declared once.

This package pre-structures those relationships as a typed dependency graph. 55 nodes. 74 edges. Served over MCP. Traversed deterministically.

---

## What traversal looks like

**"What do I need to run a managed MCP server on NemoClaw?"**

```
get_prerequisites("ManagedMCPServer")

→ ManagedMCPServer
  ├─ [ENABLES] NemoClaw                  ← the platform root
  ├─ [REQUIRES] NetworkPolicy            ← root concept — no dependencies
  └─ [REQUIRES] L7Proxy
       ├─ [IMPLEMENTS] OpenShell         ← platform layer
       └─ [REQUIRES] SharedGateway
            ├─ [ENABLES] OpenShell
            └─ [IMPLEMENTS] InferenceProvider

269 tokens · declared edges only · no inference at query time
```

Two hops. Correct path. No hallucinated deployment steps. The graph knew — the model just told you.

**"What are the three agent runtimes and what capabilities do they share?"**

```
query_ckg("OpenClaw", depth=2)
→ OpenClaw [ENABLES] NemoClaw
→ OpenClaw [ENABLES] ProgressiveToolDisclosure
→ OpenClaw [ENABLES] DeclarativeMultiAgentManifest

query_ckg("Hermes", depth=2)
→ Hermes [ENABLES] NemoClaw
→ Hermes requires HermesProvider (Nous Research)

query_ckg("LangChain_Deep_Agents_Code", depth=2)
→ LangChain_Deep_Agents_Code [ENABLES] NemoClaw
→ LangChain_Deep_Agents_Code [ENABLES] ProgressiveToolDisclosure
```

All three implement `ProgressiveToolDisclosure` — the mechanism that controls how tools are revealed to agents based on context depth. That relationship is in the graph. A RAG query on "agent runtimes" would return docs that mention each runtime separately and leave the connection to inference.

---

## Why small models specifically

Large models have seen enough training data to fake NemoClaw competence. Small models haven't. A 7B model reasoning about inference routing or security policy layers with no context isn't hallucinating — it's guessing from statistical patterns that weren't dense enough in training to stick.

CKG fixes this by injecting the **declared structure** of the domain directly into context. The model stops guessing and starts traversing.

**Local A/B test — CPU only, Ollama, same harness, no GPU:**

| Model | Bare F1 | + CKG F1 | Lift |
|-------|---------|----------|------|
| phi4-mini (2.5 GB) | 0.047 | 0.325 | **+598%** |
| nemotron-mini (4B) | 0.174 | 0.412 | **+137%** |

**phi4-mini + CKG (0.325) outperforms nemotron-mini bare (0.174) by 86%.** A laptop model with a graph beats a specialized model without one. CKG is also faster — the graph stops hallucinated generation, so Arm B averages 4.4s vs 6.7s for Arm A.

---

## Install

```bash
pip install ckg-nvidia-nemoclaw
```

## Use as a claude.ai connector (remote, no install)

Add this URL in claude.ai → Settings → Connectors:

```
https://ckg-nvidia-nemoclaw.onrender.com/mcp
```

## Use locally — Claude Desktop / Claude Code

```bash
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

---

## Tools

| Tool | Description |
|------|-------------|
| `ask_nemoclaw(question)` | Natural language query — auto-detects concept and traverses the relevant subgraph |
| `query_ckg(concept, depth)` | Typed subgraph around a specific concept (1–5 hops) |
| `get_prerequisites(concept)` | Full upstream prerequisite chain — every dependency in order |
| `search_concepts(query)` | Fuzzy search across all 55 concepts by name or keyword |
| `list_domains()` | Available domains and node/edge counts |

---

## What's in the graph

**55 nodes · 74 edges · 4 edge types: `REQUIRES` · `ENABLES` · `IMPLEMENTS` · `RELATES_TO`**

| Layer | Concepts |
|-------|----------|
| **Agent runtimes** | OpenClaw · Hermes (Nous Research) · LangChain Deep Agents Code |
| **Platform** | OpenShell · NVIDIA Agent Toolkit · OpenShell TUI · CLI |
| **Inference** | inference.local routing · SharedGateway · vLLM · Ollama · Local NIM · ModelRouter · InferenceProvider |
| **Policy** | NetworkPolicy · PolicyTier (Restricted/Balanced/Open) · PolicyPreset bundles |
| **Security** | L7 proxy · Landlock LSM · CONNECT proxy · Corporate CA · SecurityHardening · VulnerabilityReporting |
| **Agent features** | Progressive Tool Disclosure · Context Compaction · Agent Heartbeat · Snapshots · Shields |
| **Configuration** | NemoClaw Blueprint · Declarative Multi-Agent Manifest · Managed MCP Servers · Skills · Plugins |
| **Deployment** | Local CLI · Brev CLI · Brev Web UI · DGX Spark · DGX Station · macOS Apple Silicon · WSL2 |
| **Ecosystem** | FOX Blueprint · MoMClaw (Foxconn) · Nemotron 3 Ultra · Agent Harness · LKG Installer |
| **Channels** | Telegram · Discord · Slack · WeChat · WhatsApp · Teams |

Every concept maps to a source URL at `docs.nvidia.com/nemoclaw/latest/`. The graph was built from official NemoClaw docs, the FOX Blueprint, and the Nemotron 3 Ultra ecosystem documentation.

---

## Benchmark (v0.6.2 locked)

| System | Macro F1 | Mean tokens | Cost / 1k queries |
|--------|----------|-------------|-------------------|
| CKG | **0.471** | 269 | $7.81 |
| RAG | 0.123 | 2,982 | $76.23 |
| GraphRAG | 0.120 | ~3,000 | ~$76 |

7,928 queries · 5-hop F1: 0.772 (CKG) vs 0.170 (RAG)

These numbers are ours, on our benchmark. The dataset is [public on HuggingFace](https://huggingface.co/datasets/danyarm/ckg-benchmark). Run it yourself: [github.com/Yarmoluk/ckg-benchmark](https://github.com/Yarmoluk/ckg-benchmark/blob/main/paper/main.pdf)

---

Built by [Graphify.md](https://graphifymd.com) · [PyPI](https://pypi.org/project/ckg-nvidia-nemoclaw/) · patent pending
