# AI Ads Readiness Generator — Simple Python Edition

Python-only replacement for the earlier project. No Docker.

## Includes
- Public website crawler with basic SSRF protections
- Deterministic readiness scoring
- Recommendations and commercial-intent detection
- AI/LLM assets: llms.txt, llms-full.txt, ai-business.json, ai-products.json, ai-services.json, ai-faq.json, ai-use-cases.json, ai-pricing.json, ai-ad-config.json, ai-commercial-intents.json, ai-audience.json, schema.jsonld, report.json, report.md
- FastAPI REST API
- MCP Streamable HTTP endpoint at `/mcp`
- No AI API key required

## Run in VS Code / Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Put the generated value into `.env` as `MCP_API_KEY=...`.

Start:

```powershell
python -m app.main
```

Open:
- http://127.0.0.1:8000/
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/api/health
- http://127.0.0.1:8000/mcp

## First test

```powershell
$body = @{ url = "https://example.com"; max_pages = 3 } | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/analyze" -Method Post -ContentType "application/json" -Body $body
```

Use the returned `project_id` with `/api/generate?project_id=...`.

## Important
Generated readiness files do not guarantee inclusion, ranking, recommendation or ad placement in any AI platform. `ai-ad-config.json` is an application-level specification, not an official advertising API.
