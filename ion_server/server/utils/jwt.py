import jwt, datetime, uuid
from django.conf import settings

# Ожидается, что в settings.py есть:
# JWT_PRIVATE_KEY (PEM), JWT_PUBLIC_KEY (PEM), JWT_ALG="RS256", ACCESS_TTL=900, REFRESH_TTL=2592000
ALG = getattr(settings, "JWT_ALG", "RS256")
ACCESS_TTL = int(getattr(settings, "JWT_ACCESS_TTL", 900))
REFRESH_TTL = int(getattr(settings, "JWT_REFRESH_TTL", 2592000))

def issue_access(sub: str, tid: str, roles: list[str], perms: list[str], sid: str, device_id: str, extra: dict=None):
    now = datetime.datetime.utcnow()
    payload = {
        "sub": sub, "tid": tid,
        "roles": roles, "perms": perms,
        "iat": int(now.timestamp()),
        "exp": int((now + datetime.timedelta(seconds=ACCESS_TTL)).timestamp()),
        "jti": str(uuid.uuid4()),
        "sid": sid, "device_id": device_id
    }
    if extra: payload.update(extra)
    return jwt.encode(payload, settings.JWT_PRIVATE_KEY, algorithm=ALG)

def issue_refresh(sub: str, tid: str, sid: str, device_id: str):
    now = datetime.datetime.utcnow()
    payload = {
        "sub": sub, "tid": tid,
        "iat": int(now.timestamp()),
        "exp": int((now + datetime.timedelta(seconds=REFRESH_TTL)).timestamp()),
        "jti": str(uuid.uuid4()),
        "sid": sid, "device_id": device_id, "typ": "refresh"
    }
    return jwt.encode(payload, settings.JWT_PRIVATE_KEY, algorithm=ALG)

def decode_token(token: str):
    return jwt.decode(token, settings.JWT_PUBLIC_KEY, algorithms=[ALG])
