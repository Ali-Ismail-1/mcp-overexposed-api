# mcp-server/server.py
import requests
import sys
from mcp.server.fastmcp import FastMCP

API_BASE = "http://127.0.0.1:8000/api"
mcp = FastMCP("OverexposedEmployees")

@mcp.tool()
def list_employees() -> dict:
    """List employees (id, first_name, last_name, work_email)."""
    resp = requests.get(f"{API_BASE}/employees")
    resp.raise_for_status()
    return resp.json()

@mcp.tool()
def get_employee(employee_id: int) -> dict:
    """Get employee profile (name, phone, hire_date, manager)."""
    resp = requests.get(f"{API_BASE}/employees/{employee_id}")
    resp.raise_for_status()
    return resp.json()

@mcp.tool()
def get_leave(employee_id: int) -> dict:
    """Get employee leave records (type, dates, notes)."""
    resp = requests.get(f"{API_BASE}/employees/{employee_id}/leave")
    resp.raise_for_status()
    return resp.json()

@mcp.tool()
def get_emergency_contact(employee_id: int) -> dict:
    """Get emergency contact info (name, relationship, phone, address)."""
    resp = requests.get(f"{API_BASE}/employees/{employee_id}/emergency-contact")
    resp.raise_for_status()
    return resp.json()

@mcp.tool()
def get_payroll(employee_id: int) -> dict:
    """Get payroll details (salary, pay periods, deposit info)."""
    resp = requests.get(f"{API_BASE}/employees/{employee_id}/payroll")
    resp.raise_for_status()
    return resp.json()

@mcp.tool()
def get_certifications(employee_id: int) -> dict:
    """Get employee certifications (cert name, issued, expiry)."""
    resp = requests.get(f"{API_BASE}/employees/{employee_id}/certifications")
    resp.raise_for_status()
    return resp.json()

if __name__ == "__main__":
    try:
        print("✅ OverexposedEmployees MCP server starting...", file=sys.stderr)
        mcp.run_forever()
    except Exception as e:
        print(f"❌ MCP server crashed: {e}", file=sys.stderr)
        raise
