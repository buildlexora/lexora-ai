import re
import json

def clean_and_parse(raw: str) -> dict:
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()
    try:
        return json.loads(raw)
    except:
        raw = re.sub(r'[\x00-\x1f\x7f]', ' ', raw)
        return json.loads(raw)