"""
ckg-nvidia-nemoclaw — NVIDIA NemoClaw as a traversable knowledge graph.

55 nodes · 74 edges · MCP-native · 11x fewer tokens than RAG

Covers: OpenShell runtime · OpenClaw · Hermes · LangChain Deep Agents ·
        inference routing · network policy · security architecture ·
        progressive tool disclosure · managed MCP servers · deployment paths ·
        FOX Blueprint · Nemotron 3 Ultra ecosystem

Edge types: REQUIRES · ENABLES · RELATES_TO · IMPLEMENTS

Usage:
    uvx ckg-nvidia-nemoclaw                 # run as MCP server
    python -m ckg_nvidia_nemoclaw           # same

Claude Desktop config:
    {
      "mcpServers": {
        "nemoclaw": {
          "command": "uvx",
          "args": ["ckg-nvidia-nemoclaw"]
        }
      }
    }
"""
from __future__ import annotations

from mcp.server.fastmcp import FastMCP
from .graph import available_domains, load_graph, load_domain_meta, find_concept, bfs_subgraph, prerequisite_chain

DOMAIN = "nemoclaw"

_HINTS: list[str] = [
    "nemoclaw", "openclaw", "hermes", "dcode", "deep agents",
    "openshell", "sandbox", "inference.local", "l7 proxy", "landlock",
    "network policy", "policy preset", "policy tier", "shields",
    "progressive tool disclosure", "context compaction", "agent heartbeat",
    "managed mcp", "snapshot", "nemoclaw-blueprint", "brev",
    "fox blueprint", "moclaw", "nemotron", "agent harness",
    "vllm", "ollama", "nim", "model router", "shared gateway",
]

mcp = FastMCP(
    "ckg-nvidia-nemoclaw",
    instructions=(
        "NVIDIA NemoClaw CKG — 55 nodes, 74 edges covering sandboxed AI agent "
        "infrastructure. Workflow: search_concepts(query) to resolve a concept, "
        "then query_ckg(concept) for its typed subgraph or "
        "get_prerequisites(concept) for the full upstream chain. "
        "Every result traces to a declared edge — no probabilistic inference."
    ),
)

_graph_cache: tuple | None = None


def _graph():
    global _graph_cache
    if _graph_cache is None:
        _graph_cache = load_graph(DOMAIN)
    return _graph_cache


@mcp.tool()
def ask_nemoclaw(question: str) -> str:
    """Answer a question about NVIDIA NemoClaw by traversing the knowledge graph.

    Covers: agent runtimes (OpenClaw/Hermes/Deep Agents), OpenShell platform,
    inference routing, network policy, security layers, deployment paths,
    progressive tool disclosure, managed MCP servers, snapshots, shields,
    FOX Blueprint, Nemotron 3 Ultra ecosystem, and platform support.

    Args:
        question: Your question about NemoClaw concepts or architecture.
    """
    id_to_label, label_to_id, prerequisites, dependents, taxonomy = _graph()
    q = question.lower()

    hit = find_concept(label_to_id, q)
    if not hit:
        for word in q.split():
            hit = find_concept(label_to_id, word)
            if hit:
                break
    if hit:
        chain = prerequisite_chain(hit, prerequisites, id_to_label)
        subgraph = bfs_subgraph(hit, prerequisites, id_to_label, max_depth=3)
        meta = load_domain_meta(DOMAIN)
        lines = [
            f"# NemoClaw CKG — {id_to_label[hit]}",
            f"_Domain: {meta.get('description', 'NVIDIA NemoClaw')}_\n",
            "## Prerequisites",
        ]
        for label in chain:
            lines.append(f"- {label}")
        lines.append("\n## Subgraph")
        for node in subgraph:
            tax = taxonomy.get(node['concept_id'], "")
            indent = "  " * node['depth']
            etype = f" [{node['edge_type']}]" if node['edge_type'] else ""
            lines.append(f"{indent}- **{node['concept']}** [{tax}]{etype}")
        return "\n".join(lines)

    return (
        f"No exact match for '{question}' in NemoClaw CKG.\n"
        "Try search_concepts() to find the closest label, "
        "then call ask_nemoclaw() or query_ckg() with the exact name."
    )


@mcp.tool()
def query_ckg(concept: str, depth: int = 3) -> str:
    """Return the typed subgraph around a NemoClaw concept.

    Args:
        concept: Exact or partial concept label (e.g. 'OpenClaw', 'NetworkPolicy', 'L7Proxy').
        depth: Traversal hops (1–5, default 3).
    """
    id_to_label, label_to_id, prerequisites, dependents, taxonomy = _graph()
    depth = max(1, min(depth, 5))

    cid = find_concept(label_to_id, concept.lower())
    if not cid:
        return f"Concept '{concept}' not found. Use search_concepts() to find the closest match."

    chain = prerequisite_chain(cid, prerequisites, id_to_label)
    subgraph = bfs_subgraph(cid, dependents, id_to_label, max_depth=depth)
    lines = [f"## {id_to_label[cid]} (depth={depth})\n", "### Prerequisites"]
    for label in chain:
        lines.append(f"- {label}")
    lines.append("\n### Dependents")
    for node in subgraph:
        tax = taxonomy.get(node['concept_id'], "")
        indent = "  " * node['depth']
        etype = f" [{node['edge_type']}]" if node['edge_type'] else ""
        lines.append(f"{indent}- **{node['concept']}** [{tax}]{etype}")
    return "\n".join(lines)


@mcp.tool()
def get_prerequisites(concept: str) -> str:
    """Return the full upstream prerequisite chain for a NemoClaw concept.

    Useful for understanding what a concept depends on end-to-end.

    Args:
        concept: Exact or partial concept label.
    """
    id_to_label, label_to_id, prerequisites, dependents, taxonomy = _graph()
    cid = find_concept(label_to_id, concept.lower())
    if not cid:
        return f"Concept '{concept}' not found. Use search_concepts() first."

    chain = prerequisite_chain(cid, prerequisites, id_to_label)
    if len(chain) <= 1:
        return f"**{id_to_label[cid]}** has no upstream prerequisites — it is a root concept."

    lines = [f"## Prerequisite chain for {id_to_label[cid]}\n"]
    for label in chain:
        lines.append(f"- {label}")
    return "\n".join(lines)


@mcp.tool()
def search_concepts(query: str) -> str:
    """Fuzzy search for NemoClaw concepts by name or keyword.

    Args:
        query: Partial name or keyword (e.g. 'policy', 'inference', 'agent').
    """
    id_to_label, label_to_id, prerequisites, dependents, taxonomy = _graph()
    q = query.lower()
    matches = [
        (nid, label)
        for label, nid in label_to_id.items()
        if q in label
    ]
    if not matches:
        return f"No concepts matching '{query}'. Try broader terms like 'policy', 'agent', 'inference', 'security'."

    lines = [f"## Concepts matching '{query}'\n"]
    for nid, label in sorted(matches, key=lambda x: x[1]):
        tax = taxonomy.get(nid, "")
        lines.append(f"- **{label}** [{tax}] — use `query_ckg('{label}')` to traverse")
    return "\n".join(lines)


@mcp.tool()
def list_domains() -> str:
    """List available domains in this CKG server."""
    meta = load_domain_meta(DOMAIN)
    return (
        f"## Available Domains\n\n"
        f"- **nemoclaw** — {meta.get('description', '')}\n"
        f"  Nodes: {meta.get('nodes', 55)} · Edges: {meta.get('edges', 74)}\n\n"
        f"Source: docs.nvidia.com/nemoclaw/latest/ · github.com/NVIDIA/NemoClaw\n"
        f"Benchmark: github.com/Yarmoluk/ckg-benchmark/blob/main/paper/main.pdf"
    )


def main():
    mcp.run()


if __name__ == "__main__":
    main()
