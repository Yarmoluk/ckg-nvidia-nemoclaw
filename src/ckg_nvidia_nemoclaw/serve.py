"""
HTTP server for ckg-nvidia-nemoclaw — Streamable HTTP transport (Render/Smithery-compatible).
"""
from __future__ import annotations

import importlib.metadata

from .server import mcp

try:
    _VERSION = importlib.metadata.version("ckg-nvidia-nemoclaw")
except importlib.metadata.PackageNotFoundError:
    _VERSION = "dev"

_LANDING_HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ckg-nvidia-nemoclaw — NVIDIA NemoClaw Knowledge Graph</title>
  <style>
    body {{ font-family: system-ui, sans-serif; max-width: 680px; margin: 60px auto; padding: 0 24px; color: #1a1a1a; }}
    h1 {{ font-size: 1.6rem; margin-bottom: 4px; }}
    .sub {{ color: #555; margin-bottom: 8px; }}
    .tagline {{ color: #333; margin-bottom: 28px; font-size: 0.95rem; line-height: 1.5; }}
    .stats {{ display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 28px; }}
    .stat {{ background: #f0f4f8; border-radius: 6px; padding: 10px 18px; }}
    .stat strong {{ display: block; font-size: 1.3rem; }}
    .stat span {{ font-size: 0.82rem; color: #666; }}
    code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 4px; font-size: 0.92em; }}
    pre {{ background: #f4f4f4; padding: 16px; border-radius: 8px; overflow-x: auto; font-size: 0.88rem; }}
    a {{ color: #0f6e56; }}
    .badge {{ display: inline-block; background: #0f6e56; color: white; padding: 3px 10px; border-radius: 12px; font-size: 0.78rem; font-weight: 600; }}
    .license {{ font-size: 0.82rem; color: #888; margin-top: 32px; padding-top: 16px; border-top: 1px solid #eee; }}
  </style>
</head>
<body>
  <a href="https://yarmoluk.github.io/ckg-nvidia-nemoclaw">
    <img src="https://raw.githubusercontent.com/Yarmoluk/ckg-nvidia-nemoclaw/main/assets/og.png"
         alt="ckg-nvidia-nemoclaw" style="width:100%;border-radius:8px;margin-bottom:24px;display:block"/>
  </a>
  <h1>ckg-nvidia-nemoclaw <span class="badge">v{_VERSION}</span></h1>
  <p class="sub">Auditable knowledge graph · NVIDIA NemoClaw · built by <a href="https://graphifymd.com">Graphify.md</a></p>
  <p class="tagline">
    Every edge traces to a declared relationship and a SHA-256-pinned source document.<br>
    Deterministic agent answers — no inference at query time.
  </p>

  <div class="stats">
    <div class="stat"><strong>55</strong><span>nodes</span></div>
    <div class="stat"><strong>74</strong><span>edges</span></div>
    <div class="stat"><strong>269</strong><span>avg tokens</span></div>
    <div class="stat"><strong>0.471</strong><span>F1 · 4× RAG</span></div>
    <div class="stat"><strong>11×</strong><span>fewer tokens than RAG</span></div>
  </div>

  <h2>Connect</h2>
  <p><strong>claude.ai connector URL:</strong></p>
  <pre>https://ckg-nvidia-nemoclaw.onrender.com/mcp</pre>
  <p>Settings → Connectors → Add connector → paste URL.</p>

  <p><strong>Claude Desktop / Claude Code:</strong></p>
  <pre>{{
  "mcpServers": {{
    "nemoclaw": {{
      "command": "uvx",
      "args": ["ckg-nvidia-nemoclaw"]
    }}
  }}
}}</pre>

  <h2>Tools</h2>
  <ul>
    <li><code>ask_nemoclaw(question)</code> — natural language query over the graph</li>
    <li><code>query_ckg(concept, depth)</code> — typed subgraph traversal (1–5 hops)</li>
    <li><code>get_prerequisites(concept)</code> — full upstream dependency chain</li>
    <li><code>search_concepts(query)</code> — fuzzy search across all 55 concepts</li>
    <li><code>list_domains()</code> — available domains and node/edge counts</li>
    <li><code>verify_source(concept)</code> — source URL + SHA-256 hash · full audit chain</li>
  </ul>

  <h2>Install</h2>
  <pre>pip install ckg-nvidia-nemoclaw
# or: uvx ckg-nvidia-nemoclaw</pre>

  <p>
    <a href="https://github.com/Yarmoluk/ckg-nvidia-nemoclaw">GitHub</a> ·
    <a href="https://pypi.org/project/ckg-nvidia-nemoclaw/">PyPI</a> ·
    <a href="https://github.com/Yarmoluk/ckg-benchmark/blob/main/paper/main.pdf">Benchmark paper</a> ·
    <a href="https://yarmoluk.github.io/ckg-nvidia-nemoclaw">Interactive graph</a>
  </p>

  <p class="license">
    Code: MIT · Data: Elastic License 2.0 · Pipeline: Proprietary — Graphify.md<br>
    Community-built. Not affiliated with NVIDIA Corporation. NemoClaw is a trademark of NVIDIA Corporation.
  </p>
</body>
</html>"""


def main():
    import os
    import sys

    port = 8000
    for i, arg in enumerate(sys.argv):
        if arg == "--port" and i + 1 < len(sys.argv):
            port = int(sys.argv[i + 1])
    port = int(os.environ.get("PORT", port))

    from starlette.applications import Starlette
    from starlette.requests import Request
    from starlette.responses import HTMLResponse, JSONResponse
    from starlette.routing import Mount, Route
    import uvicorn

    async def homepage(request: Request):
        return HTMLResponse(_LANDING_HTML)

    async def server_card(request: Request):
        return JSONResponse({
            "name": "ckg-nvidia-nemoclaw",
            "version": _VERSION,
            "description": "Auditable knowledge graph for NVIDIA NemoClaw — cryptographic source traceability, MCP-native",
            "tools": [
                "ask_nemoclaw", "query_ckg", "get_prerequisites",
                "search_concepts", "list_domains", "verify_source",
            ],
            "publisher": "Graphify.md",
            "publisher_url": "https://graphifymd.com",
            "license": "Elastic-2.0 (data) / MIT (code)",
        })

    mcp_app = mcp.streamable_http_app()

    app = Starlette(
        routes=[
            Route("/", homepage),
            Route("/.well-known/mcp/server-card.json", server_card),
            Mount("/mcp", app=mcp_app),
        ],
        redirect_slashes=False,
    )

    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
