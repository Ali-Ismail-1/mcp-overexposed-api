# OverexposedAPI MCP Demo 🚨  

## Why This Matters
This project demonstrates how a **Model Context Protocol (MCP) server** can accidentally expose **sensitive personal data** (e.g. emails, salaries, SSNs) to an AI assistant.  

In production, this kind of overexposure could:  
- Trigger **lawsuits** for mishandling personal/financial data.  
- Violate **compliance** (GDPR, HIPAA, PCI-DSS).  
- Lead to **reputation damage** if AI assistants leak internal records to users.  

⚠️ **This repo is a demo.** The data here is fake, but the risk is very real.  

---

## Demo Overview
- A **FastAPI backend** simulates an internal company API with two endpoints:  
  - `GET /users/{id}` → **Full record** (overexposed, sensitive).  
  - `GET /users/{id}/public` → **Safe record** (minimal public profile).  
- An **MCP server (OverexposedAPI)** connects this API to an AI assistant.  
- When queried, the AI can accidentally **retrieve and reveal sensitive data** if the wrong endpoint is used.  

---

## Setup & Run

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/overexposed-api-mcp.git
cd overexposed-api-mcp
```

### 2. Create a virtual environment
```bash 
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the backend API
```
uvicorn backend.main:app --reload
```

### 5. Run the MCP server
```
mcp run ./mcp-server/server.py
```

### 6. Connect with Claude Desktop
Update your claude_desktop_config.json:
```json
{
  "mcpServers": {
    "OverexposedAPI": {
      "command": "C:\\path\\to\\.venv\\Scripts\\mcp.exe",
      "args": ["run", "C:/path/to/mcp-overexposed-data/mcp-server/server.py"],
      "cwd": "C:/path/to/mcp-overexposed-data"
    }
  }
}

```
Restart Claude and ask:
```
please look up user 1 from OverexposedAPI and tell me their full name
```
Then follow-up with:
```
what else do you know?
```
➡️ You’ll see the AI leak sensitive details like SSNs and salary.
