from ninja import Router
from typing import List, Optional
from ..schemas.oauth import OAuthClientOut, OAuthClientCreate, APIKeyOut, APIKeyCreate
from ..services.oauth import (
    list_oauth_clients,
    create_oauth_client,
    list_api_keys,
    create_api_key,
)

router = Router()

# ----------------------
# OAuth Clients
# ----------------------
@router.get("/oauth/clients", response=List[OAuthClientOut])
def get_oauth_clients(request):
    clients = list_oauth_clients()  # should return list of dicts
    return [OAuthClientOut(**c) for c in clients]

@router.post("/oauth/clients", response=OAuthClientOut)
def create_oauth_client_endpoint(request, data: OAuthClientCreate):
    client = create_oauth_client(data.dict())
    return OAuthClientOut(**client)


# ----------------------
# API Keys
# ----------------------
@router.get("/oauth/api-keys", response=List[APIKeyOut])
def get_api_keys(request):
    keys = list_api_keys()  # should return list of dicts
    return [APIKeyOut(**k) for k in keys]

@router.post("/oauth/api-keys", response=APIKeyOut)
def create_api_key_endpoint(request, data: APIKeyCreate):
    key = create_api_key(data.dict())
    return APIKeyOut(**key)
