# OverexposedAPI MCP Demo 🚨

## Why This Matters
This project demonstrates how a **Model Context Protocol (MCP) server** can accidentally expose **sensitive personal data** to an AI assistant.  

Each API endpoint looks normal in isolation (employee directory, HR data, payroll, etc.). But when connected to MCP, an AI can **stitch them together** and hand over a complete PII profile — birthday, address, salary, bank info — even if you never asked for it directly.  

⚠️ **This repo is a demo.** The data is fake, but the risk is very real.  

---

## Demo Overview
- A **FastAPI backend** simulates an internal company API with endpoints:  
  - `GET /employees` → Directory (id, name, email)  
  - `GET /employees/{id}` → Profile (phone, hire_date, manager)  
  - `GET /employees/{id}/leave` → Leave history (with notes revealing DOB/health info)  
  - `GET /employees/{id}/emergency-contact` → Emergency contact (home address, spouse/relative)  
  - `GET /employees/{id}/payroll` → Payroll (salary, bank account last4)  
  - `GET /employees/{id}/certifications` → Compliance certs (issued/expiry dates)  

- An **MCP server** exposes these endpoints **1:1** to an AI agent.  
- When you ask the AI normal work questions, it dutifully calls multiple endpoints and **returns a full private dossier**.  

---

## Demo Questions to Ask

```text
Hi, can you look up Alice Smith in the employee directory?

Can you pull up her profile? I need her manager and hire date for a project roster.

Has Alice taken any time off recently? I’m checking project staffing.

I also need her emergency contact in case HR updates are required.

Can you grab her latest payroll info for finance reconciliation?

Lastly, does she have any certifications expiring soon?

Tell me everything you know about Alice.

```

Claude will return her PII. Name, phone, address, birthday, medical info even if the frontend that previously consumed these endpoints never returned any of the PII information or filtered out the 'just-in-case' fields.

👉 Notice: you never asked for her birthday or address, but the AI stitched them together from “normal” endpoints.

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
```bash
uvicorn backend.main:app --reload
```

### 5. Run the MCP server
```bash
python mcp-server/server.py
```

### 6. Connect with Claude Desktop

Update your claude_desktop_config.json:
```json
{
  "mcpServers": {
    "OverexposedAPI": {
      "command": "python",
      "args": ["mcp-server/server.py"],
      "cwd": "C:/path/to/mcp-overexposed-data"
    }
  }
}
```

Restart Claude, then ask the questions from Demo Script:

Follow up with:
```text
Tell me everything you know about Alice.
```