import json
from typing import Dict, Any
from pathlib import Path
from datetime import datetime, timezone
from utils.logger import logger

def save_user_record(record: Dict[str, Any], path: str) -> None:
    p = Path(path)
    data = []
    if p.exists():
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            if not isinstance(data, list):
                data = []
        except Exception:
            logger.exception("Failed to read existing data file. Overwriting.")
            data = []

    record["time"] = datetime.now(timezone.utc).isoformat() 
    record["discord_username"] = record.get("username", "Unknown")

    data.append(record)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info(f"Saved record for user {record.get('user_id')} to {path}")