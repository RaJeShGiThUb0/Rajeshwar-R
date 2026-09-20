"""CSV -> bronze ingestion.

The production version writes the raw file to GCS. The local mode copies it
into data/bronze so the project remains runnable without cloud credentials.
"""
from pathlib import Path
import shutil

def ingest_csv(source: str, bronze_dir: str = "data/bronze") -> str:
    src = Path(source)
    if not src.exists():
        raise FileNotFoundError(source)
    target_dir = Path(bronze_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / src.name
    shutil.copy2(src, target)
    return str(target)

if __name__ == "__main__":
    print(ingest_csv("data/sample/orders.csv"))
