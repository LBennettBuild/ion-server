from ninja import Schema
from typing import List, Optional


class OAuthClientOut(Schema):
    id: str
    name: str
    type: str
    redirect_uris: List[str]
    scopes: List[str]

class OAuthClientCreate(Schema):
    name: str
    redirect_uris: List[str]
    scopes: List[str]
    type: str  # confidential/public

class APIKeyOut(Schema):
    id: str
    name: str
    scopes: List[str]
    created_at: str
    revoked_at: Optional[str] = None
    masked_key: str

class APIKeyCreate(Schema):
    name: str
    scopes: List[str]
