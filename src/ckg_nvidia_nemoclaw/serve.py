"""
HTTP server for ckg-nvidia-nemoclaw — Streamable HTTP transport (Render/Smithery-compatible).
"""
from __future__ import annotations

import importlib.metadata
import os
import time
import uuid
import threading
from collections import defaultdict

from .server import mcp
from .analytics import track

_FREE_LIMIT = 5
_TRIAL_LIMIT = 100
_STRIPE_LINK = "https://buy.stripe.com/fZu9ATccIgCg4FO9iQ1kA06"
_CAL_LINK = "https://cal.com/daniel-yarmoluk-sjmnub/30min"
_TALLY_LINK = "https://tally.so/r/ckg-trial"

_call_counts: dict = defaultdict(lambda: {"count": 0, "reset": time.time() + 86400})
_trial_keys: dict = {}


def _get_ip(request) -> str:
    forwarded = request.headers.get("X-Forwarded-For", "")
    return forwarded.split(",")[0].strip() if forwarded else (request.client.host or "unknown")


def _check_rate_limit(ip: str) -> bool:
    now = time.time()
    state = _call_counts[ip]
    if now > state["reset"]:
        state["count"] = 0
        state["reset"] = now + 86400
    if state["count"] >= _FREE_LIMIT:
        return False
    state["count"] += 1
    return True


def _send_trial_email(email: str, key: str) -> None:
    resend_key = os.environ.get("RESEND_KEY", "")
    if not resend_key:
        return
    try:
        import httpx
        httpx.post(
            "https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {resend_key}"},
            json={
                "from": "Graphify.md <noreply@graphifymd.com>",
                "to": [email],
                "subject": "Your CKG trial key",
                "html": (
                    f"<p>Thanks for registering!</p>"
                    f"<p><strong>Trial key:</strong> <code>{key}</code></p>"
                    f"<p>Add to your MCP client as the <code>X-License-Key</code> header. "
                    f"Gives you 100 calls on the ckg-nvidia-nemoclaw endpoint.</p>"
                    f"<p>Endpoint: <code>https://ckg-nvidia-nemoclaw.onrender.com/mcp</code></p>"
                    f"<p>— Graphify.md</p>"
                ),
            },
            timeout=5.0,
        )
    except Exception:
        pass

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
    import sys

    port = 8000
    for i, arg in enumerate(sys.argv):
        if arg == "--port" and i + 1 < len(sys.argv):
            port = int(sys.argv[i + 1])
    port = int(os.environ.get("PORT", port))

    from starlette.applications import Starlette
    from starlette.middleware.base import BaseHTTPMiddleware
    from starlette.requests import Request
    from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse
    from starlette.routing import Mount, Route
    import uvicorn

    class RateLimitMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request, call_next):
            if request.url.path.startswith("/mcp"):
                ip = _get_ip(request)
                license_key = request.headers.get("X-License-Key", "").strip()
                if license_key:
                    entry = _trial_keys.get(license_key)
                    if entry is None or entry["calls"] >= _TRIAL_LIMIT:
                        return JSONResponse(
                            {"error": "Trial limit reached.", "subscribe": _STRIPE_LINK},
                            status_code=402,
                        )
                    entry["calls"] += 1
                    track("ckg-nvidia-nemoclaw", "mcp_request", {"key_type": "trial", "_ip": ip})
                else:
                    if not _check_rate_limit(ip):
                        track("ckg-nvidia-nemoclaw", "rate_limit_hit", {"_ip": ip})
                        return JSONResponse(
                            {
                                "error": f"Free tier limit reached ({_FREE_LIMIT} calls/day).",
                                "get_trial_key": _TALLY_LINK,
                                "subscribe": _STRIPE_LINK,
                            },
                            status_code=402,
                        )
                    track("ckg-nvidia-nemoclaw", "mcp_request", {"key_type": "free", "_ip": ip})
            return await call_next(request)

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

    async def register(request: Request):
        email = ""
        if request.method == "POST":
            try:
                body = await request.json()
                if "data" in body and "fields" in body["data"]:
                    for field in body["data"]["fields"]:
                        if "email" in (field.get("label") or "").lower() or field.get("type") == "INPUT_EMAIL":
                            email = field.get("value", "")
                            break
                else:
                    email = body.get("email", "")
            except Exception:
                email = request.query_params.get("email", "")
        else:
            email = request.query_params.get("email", "")

        if not email or "@" not in email:
            return JSONResponse({"error": "valid email required"}, status_code=400)

        key = uuid.uuid4().hex[:24]
        _trial_keys[key] = {"email": email, "calls": 0}
        track("ckg-nvidia-nemoclaw", "trial_register", {"email": email})
        threading.Thread(target=_send_trial_email, args=(email, key), daemon=True).start()
        return JSONResponse({
            "key": key,
            "email": email,
            "limit": _TRIAL_LIMIT,
            "header": "X-License-Key",
            "endpoint": "https://ckg-nvidia-nemoclaw.onrender.com/mcp",
        })

    async def mcp_redirect(request: Request):
        return RedirectResponse(url="/mcp/", status_code=308)

    mcp_app = mcp.streamable_http_app()

    app = Starlette(routes=[
        Route("/", homepage),
        Route("/.well-known/mcp/server-card.json", server_card),
        Route("/register", register, methods=["GET", "POST"]),
        Route("/mcp", mcp_redirect),
        Mount("/mcp/", app=mcp_app),
    ])
    app.add_middleware(RateLimitMiddleware)

    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
