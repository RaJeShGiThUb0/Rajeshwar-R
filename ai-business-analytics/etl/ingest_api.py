"""REST API ingestion with basic retry handling."""
import time
import requests

def fetch_json(url: str, retries: int = 3, timeout: int = 30):
    last_error = None
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            last_error = exc
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
    raise RuntimeError(f"API ingestion failed: {last_error}") from last_error
