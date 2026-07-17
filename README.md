<!-- mcp-name: io.github.Yarmoluk/ckg-nvidia-nemoclaw -->

<div align="center">

# ckg-nvidia-nemoclaw

### NVIDIA NemoClaw as a traversable knowledge graph — MCP-native

**NemoClaw shows you which agent is burning your budget. CKG reduces the burn.**

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

## The graph

```mermaid
graph TD
    NC[NemoClaw] --> OS[OpenShell]
    NC --> OC[OpenClaw]
    NC --> HM[Hermes]
    NC --> LC[LangChain Deep Agents]
    NC --> MCP[ManagedMCPServer]
    NC --> AH[AgentHeartbeat]

    OC --> PTD[ProgressiveToolDisclosure]
    HM --> PTD
    LC --> PTD

    OS --> L7[L7Proxy]
    OS --> LL[LandlockLSM]
    OS --> CP[CONNECT_Proxy]

    L7 --> SG[SharedGateway]
    SG --> IP[InferenceProvider]
    IP --> vLLM[vLLM]
    IP --> OLL[Ollama]
    IP --> NIM[NIM_Local]
    IP --> MR[ModelRouter]

    MCP --> NP[NetworkPolicy]
    MCP --> L7

    NP --> PT[PolicyTier]
    NP --> PP[PolicyPreset]
    PP --> TG[Telegram]
    PP --> DC[Discord]
    PP --> SL[Slack]

    SH[SecurityHardening] --> SB[Sandbox]
    SH --> LL
    SH --> BP[NemoClaw_Blueprint]

    NIM --> DGX[DGX_Spark]

    style NC fill:#0f6e56,color:#fff
    style PTD fill:#1a5c47,color:#fff
    style SH fill:#1a5c47,color:#fff
    style NP fill:#1a5c47,color:#fff
    style IP fill:#2d7a5e,color:#fff
```

---

## What developers are actually hitting

Across GitHub issues, HN threads, and hands-on walkthroughs, three NemoClaw pain signals dominate:

**1. Context bloat in tool loops.** Agents using OpenClaw, Hermes, or LangChain Deep Agents accumulate context across tool calls until the window fills and the session degrades. The bloat isn't the tools — it's that the model re-infers NemoClaw's architecture on every query instead of reading it from a declared structure.

**2. "Which agent is burning my budget?"** Routing inference through OpenShell makes token spend visible per agent for the first time — developers can suddenly see the burn. The next question is how to reduce it.

**3. The Policy Source Gap.** NVIDIA's own OpenShell knowledge graph names this explicitly: `Policy Source Gap` — the missing layer between the runtime policy engine and the structured domain knowledge agents need to make compliant decisions. The graph declares the gap. We filled it.

This package is that layer.

---

## What it is

55 nodes · 74 edges · the full NemoClaw stack as a typed dependency graph. Pre-structured, traversable, deterministic. Served over MCP. No inference at query time — the graph declares relationships that the model traverses instead of infers.

```
Agent asks: "What do I need to deploy a managed MCP server on NemoClaw?"

CKG returns:
  ManagedMCPServer
  ├─ [ENABLES]  NemoClaw               ← platform root
  ├─ [REQUIRES] NetworkPolicy          ← root concept, no dependencies
  └─ [REQUIRES] L7Proxy
       ├─ [IMPLEMENTS] OpenShell
       └─ [REQUIRES]   SharedGateway
            ├─ [ENABLES]     OpenShell
            └─ [IMPLEMENTS]  InferenceProvider

  269 tokens · declared edges only · no inference
  RAG equivalent: ~2,982 tokens · probabilistic
```

```
Agent asks: "What are the three agent runtimes and what do they share?"

  OpenClaw              → [ENABLES] ProgressiveToolDisclosure
  Hermes                → [ENABLES] ProgressiveToolDisclosure
  LangChain_Deep_Agents → [ENABLES] ProgressiveToolDisclosure

  All three implement the same disclosure mechanism.
  A RAG query returns three separate docs. The connection requires inference.
  The graph knows — it's a declared edge.
```

---

## Why zero inference matters for NemoClaw specifically

The dominant community skepticism about NemoClaw: *"even local mode still demands an NVIDIA API key"* — the inference pipeline is cloud-connected regardless of configuration.

CKG runs on **pure Python BFS**. No model. No inference. No API key. No cloud. The graph structure is the answer — the model traverses it, it doesn't generate it. This is what "the graph doesn't guess — it traverses" actually means at the implementation level.

This also makes it suitable for the use cases NemoClaw is specifically designed for: air-gapped deployments, sovereign infrastructure, edge hardware.

---

## The Sandbox Container dependency chain

NemoClaw's sandbox is built to contain the tools your developers already use — the OpenShell CKG declares this explicitly:

```
Sandbox Container
  ├─ [REQUIRES] Gateway
  │    └─ [REQUIRES] OpenShell Runtime
  └─ [REQUIRES] K3s Kubernetes

  [ENABLES] Claude Code
  [ENABLES] OpenCode / Codex
  [ENABLES] GitHub Copilot CLI
  [ENABLES] Cursor
  [ENABLES] Ollama (community)
```

When those agents run inside NemoClaw's blast radius, they need to reason about NemoClaw's architecture — routing, policy tiers, inference providers, security layers. That's exactly what this graph is for.

---

## Why small models specifically

Large models fake domain competence. Small models guess. A 7B model reasoning about NemoClaw's inference routing or security policy tiers without structured context isn't hallucinating — it's producing statistical patterns that weren't dense enough in training to stick.

CKG injects the **declared structure** of the domain directly into context. The model stops guessing, starts traversing.

**Local A/B test — CPU only, Ollama, same harness, no GPU:**

| Model | Bare F1 | + CKG F1 | Lift |
|-------|---------|----------|------|
| phi4-mini (2.5 GB) | 0.047 | 0.325 | **+598%** |
| nemotron-mini (4B) | 0.174 | 0.412 | **+137%** |

phi4-mini + CKG (0.325) beats nemotron-mini bare (0.174) by **86%**. A 2.5 GB laptop model with a graph outperforms a 4B specialized model without one.

CKG is also faster: 4.4s average vs 6.7s bare — the graph stops hallucinated generation before it starts.

---

## Install

```bash
pip install ckg-nvidia-nemoclaw
```

## Use as a claude.ai connector (remote, no install)

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
| `ask_nemoclaw(question)` | Natural language query — auto-detects concept, traverses the relevant subgraph |
| `query_ckg(concept, depth)` | Typed subgraph around a specific concept (1–5 hops) |
| `get_prerequisites(concept)` | Full upstream prerequisite chain — every dependency in order |
| `search_concepts(query)` | Fuzzy search across all 55 concepts |
| `list_domains()` | Available domains and node/edge counts |

---

## What's in the graph

**55 nodes · 74 edges · 4 edge types: `REQUIRES` · `ENABLES` · `IMPLEMENTS` · `RELATES_TO`**

| Layer | Concepts |
|-------|----------|
| **Agent runtimes** | OpenClaw · Hermes (Nous Research) · LangChain Deep Agents Code |
| **Platform** | OpenShell · NVIDIA Agent Toolkit · OpenShell TUI · CLI |
| **Inference** | inference.local routing · SharedGateway · vLLM · Ollama · Local NIM · ModelRouter |
| **Policy** | NetworkPolicy · PolicyTier (Restricted/Balanced/Open) · PolicyPreset bundles |
| **Security** | L7 proxy · Landlock LSM · CONNECT proxy · Corporate CA · SecurityHardening |
| **Agent features** | Progressive Tool Disclosure · Context Compaction · Agent Heartbeat · Snapshots · Shields |
| **Configuration** | NemoClaw Blueprint · Declarative Multi-Agent Manifest · Managed MCP Servers · Skills · Plugins |
| **Deployment** | Local CLI · Brev CLI · Brev Web UI · DGX Spark · DGX Station · macOS Apple Silicon · WSL2 |
| **Ecosystem** | FOX Blueprint · MoMClaw (Foxconn) · Nemotron 3 Ultra · Agent Harness · LKG Installer |

Every concept maps to a source URL at `docs.nvidia.com/nemoclaw/latest/`. Built from official NemoClaw docs, the FOX Blueprint, and the Nemotron 3 Ultra ecosystem.

---

## Benchmark (v0.6.2 locked)

| System | Macro F1 | Mean tokens | Cost / 1k queries |
|--------|----------|-------------|-------------------|
| CKG | **0.471** | 269 | $7.81 |
| RAG | 0.123 | 2,982 | $76.23 |
| GraphRAG | 0.120 | ~3,000 | ~$76 |

7,928 queries · 5-hop F1: 0.772 (CKG) vs 0.170 (RAG)

Dataset is public: [huggingface.co/datasets/danyarm/ckg-benchmark](https://huggingface.co/datasets/danyarm/ckg-benchmark). Run it yourself.

[Full benchmark paper →](https://github.com/Yarmoluk/ckg-benchmark/blob/main/paper/main.pdf)

---

Built by [Graphify.md](https://graphifymd.com) · [PyPI](https://pypi.org/project/ckg-nvidia-nemoclaw/) · patent pending
