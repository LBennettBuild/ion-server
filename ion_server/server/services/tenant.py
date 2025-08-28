from ..models import Tenant

# Tenant Profile
def get_profile(tenant_id: str):
    tenant = Tenant.objects.get(id=tenant_id)
    return {
        "company_name": tenant.company_name,
        "inn": tenant.inn,
        "activity_type": tenant.activity_type
    }

def update_profile(tenant_id: str, data: dict):
    tenant = Tenant.objects.get(id=tenant_id)
    for field, value in data.items():
        if value is not None:
            setattr(tenant, field, value)
    tenant.save()
    return {
        "company_name": tenant.company_name,
        "inn": tenant.inn,
        "activity_type": tenant.activity_type
    }


# Security Settings
def get_security_settings(tenant_id: str):
    tenant = Tenant.objects.get(id=tenant_id)
    return tenant.settings_security or {
        "mfa": {},
        "session": {},
        "bruteforce": {}
    }

def update_security_settings(tenant_id: str, data: dict):
    tenant = Tenant.objects.get(id=tenant_id)
    settings = tenant.settings_security or {}
    for key in ["mfa", "session", "bruteforce"]:
        if key in data and data[key] is not None:
            settings[key] = data[key]
    tenant.settings_security = settings
    tenant.save()
    return tenant.settings_security
