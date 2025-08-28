from ninja import Schema
from typing import Optional, List, Dict, Any

class TenantProfileOut(Schema):
    company_name: str
    inn: str
    activity_type: str

class TenantProfileUpdate(Schema):
    company_name: Optional[str] = None
    inn: Optional[str] = None
    activity_type: Optional[str] = None

class SecuritySettingsOut(Schema):
    mfa: Dict[str, Any]   # {required, methods, enforce_roles}
    session: Dict[str, Any]  # {ttl_minutes_by_role, remember_device_days}
    bruteforce: Dict[str, Any]  # {max_failed_attempts, lock_minutes}

class SecuritySettingsUpdate(Schema):
    mfa: Optional[Dict[str, Any]] = None
    session: Optional[Dict[str, Any]] = None
    bruteforce: Optional[Dict[str, Any]] = None
