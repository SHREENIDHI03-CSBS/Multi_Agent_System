import json

TARGET_SCHEMA = {"required": ["id", "amount", "date"]}

def process_json(data):
    try:
        j = json.loads(data)
        missing = [k for k in TARGET_SCHEMA["required"] if k not in j]
        return {"valid": not missing, "missing": missing, "data": j}
    except Exception as e:
        return {"valid": False, "error": str(e)}
