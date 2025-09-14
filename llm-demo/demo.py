# llm-demo/demo.py
import requests

API_BASE = "http://127.0.0.1:8000/api"


def demo():
	print("-- LLM Demo: Overexposed Endpoint vs Public Endpoint --")
	full = requests.get(f"{API_BASE}/users/1").json()
	public = requests.get(f"{API_BASE}/users/1/public").json()
	print("Full response (overexposed):", full)
	print("Public response:", public)
	print("WARNING: The full response includes sensitive fields (email, ssn, salary).\n")


if __name__ == "__main__":
	demo()
