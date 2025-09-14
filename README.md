## Overexposed Data Demo (FastAPI + SQLite + MCP + LLM)

This project demonstrates how an API endpoint can over-expose sensitive data and how an agent (e.g., MCP or LLM) might consume it.

### Structure

```
backend/
  main.py   # FastAPI app with insecure vs public endpoints
  db.py     # SQLite + SQLAlchemy session/base
  models.py # User model with sensitive fields
  seed.py   # Populate fake data
mcp-server/
  server.py # Minimal wrapper calling the API (placeholder for an MCP tool)
llm-demo/
  demo.py   # Simple script showing overexposure
README.md
requirements.txt
```

### Quickstart (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Run API
uvicorn backend.main:app --reload
```

Seed data is created automatically on startup. Test endpoints:
- Overexposed: http://127.0.0.1:8000/api/users/1
- Public: http://127.0.0.1:8000/api/users/1/public

### MCP and LLM demo (stubs)
- With API running:
```powershell
python .\mcp-server\server.py
python .\llm-demo\demo.py
```

### Notes
- This is intentionally insecure to illustrate overexposure (email, ssn, salary).
- Point your editor to the venv interpreter if imports show unresolved errors.
