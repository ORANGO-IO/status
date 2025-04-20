import uuid
from datetime import datetime, timezone

def generate_uuid():
    return str(uuid.uuid4())

def now_utc():
    return datetime.now(timezone.utc)