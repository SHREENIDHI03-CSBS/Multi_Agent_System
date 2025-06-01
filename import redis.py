import redis
import json

# Connect to Redis (make sure Redis server is running)
r = redis.Redis(host='localhost', port=6379, db=0)

def save_context(conversation_id, data):
    r.set(conversation_id, json.dumps(data))

def get_context(conversation_id):
    val = r.get(conversation_id)
    return json.loads(val) if val else None
