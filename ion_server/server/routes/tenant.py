from ninja import Router
from ..schemas.tenant import TenantProfileOut, TenantProfileUpdate, SecuritySettingsOut, SecuritySettingsUpdate
from ..services.tenant import (
    get_profile,
    update_profile as update_tenant_profile,
    get_security_settings,
    update_security_settings
)
from ninja.errors import HttpError

router = Router()

# ----------------------
# Tenant Profile
# ----------------------
@router.get("/tenant/profile", response=TenantProfileOut)
def tenant_profile(request):
    tenant_id = request.headers.get("X-Tenant-ID")  # or extract from auth token
    if not tenant_id:
        raise HttpError(400, "X-Tenant-ID header is required")

    try:
        profile = get_profile(tenant_id)
    except Exception:
        raise HttpError(404, f"Tenant with id {tenant_id} not found")

    return profile

@router.put("/tenant/profile", response=TenantProfileOut)
def tenant_profile_update(request, data: TenantProfileUpdate):
    tenant_id = request.headers.get("X-Tenant-ID")
    updated = update_tenant_profile(tenant_id, data.dict())
    return updated


# ----------------------
# Security Settings
# ----------------------
@router.get("/tenant/security", response=SecuritySettingsOut)
def tenant_security(request):
    tenant_id = request.headers.get("X-Tenant-ID")
    settings = get_security_settings(tenant_id)
    return settings

@router.put("/tenant/security", response=SecuritySettingsOut)
def tenant_security_update(request, data: SecuritySettingsUpdate):
    tenant_id = request.headers.get("X-Tenant-ID")
    updated_settings = update_security_settings(tenant_id, data.dict())
    return updated_settings
