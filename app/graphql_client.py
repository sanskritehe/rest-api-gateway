import requests
from typing import Dict, Any


def run_query(query: str, variables: Dict[str, Any] = {}) -> Dict[str, Any]:
    url = "http://localhost:4000"
    payload: Dict[str, Any] = {"query": query}
    if variables:
        payload["variables"] = variables
    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise RuntimeError(f"Failed to query GraphQL Datagraph: {str(e)}") from e
