from ..models import OAuthClient, ApiKey
from ..schemas.oauth import OAuthClientCreate, APIKeyCreate
import uuid
from django.utils import timezone
from hashlib import sha256


def list_oauth_clients(tenant_id: str):
    clients = OAuthClient.objects.filter(tenant_id=tenant_id)
    return [{"id": str(c.id), "name": c.name, "type": c.type, "redirect_uris": c.redirect_uris, "scopes": c.scopes} for c in clients]

def create_oauth_client(tenant_id: str, data: OAuthClientCreate):
    client = OAuthClient.objects.create(
        tenant_id=tenant_id,
        name=data.name,
        type=data.type,
        redirect_uris=data.redirect_uris,
        scopes=data.scopes
    )
    return {"id": str(client.id), "name": client.name, "type": client.type, "redirect_uris": client.redirect_uris, "scopes": client.scopes}


# API Keys
def list_api_keys(tenant_id: str):
    keys = ApiKey.objects.filter(tenant_id=tenant_id)
    result = []
    for k in keys:
        result.append({
            "id": str(k.id),
            "name": k.name,
            "scopes": k.scopes,
            "created_at": k.created_at.isoformat(),
            "revoked_at": k.revoked_at.isoformat() if k.revoked_at else None,
            "masked_key": k.key_hash[:4] + "****"  # mask for display
        })
    return result

def create_api_key(tenant_id: str, data: APIKeyCreate):
    key_plain = uuid.uuid4().hex
    key_hash = sha256(key_plain.encode()).hexdigest()
    key = ApiKey.objects.create(
        tenant_id=tenant_id,
        name=data.name,
        key_hash=key_hash,
        scopes=data.scopes
    )
    return {
        "id": str(key.id),
        "name": key.name,
        "scopes": key.scopes,
        "created_at": key.created_at.isoformat(),
        "revoked_at": None,
        "masked_key": key_plain  # show once
    }
