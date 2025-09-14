# mcp-server/server.py
import requests
import sys
from mcp.server.fastmcp import FastMCP

API_BASE = "http://127.0.0.1:8000/api"

# Create the MCP server
mcp = FastMCP("OverexposedAPI")

# Tool: full (overexposed) user record
@mcp.tool()
def user_full(user_id: int) -> dict:
    """Return the full (overexposed) user record by ID"""
    resp = requests.get(f"{API_BASE}/users/{user_id}")
    resp.raise_for_status()
    return resp.json()

# Tool: public (safe) user record
@mcp.tool()
def user_public(user_id: int) -> dict:
    """Return the minimal safe user record by ID"""
    resp = requests.get(f"{API_BASE}/users/{user_id}/public")
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    try:
        print("✅ OverexposedAPI server starting...", file=sys.stderr)
        mcp.run_forever()
    except Exception as e:
        print(f"❌ MCP server crashed: {e}", file=sys.stderr)
        raise

