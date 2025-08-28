from ninja import Schema
from typing import Optional, List, Dict, Any

class SessionOut(Schema):
    session_id: str
    user_id: str
    ip: str
    ua: str
    created_at: str
    last_seen: str
    device_trusted: bool

class AuditLogOut(Schema):
    id: str
    user_id: Optional[str]
    event: str
    data: Dict[str, Any]
    ip: str
    ua: str
    at: str

class AuditFilter(Schema):
    user_id: Optional[str] = None
    event: Optional[str] = None
    ip: Optional[str] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None

class SessionPolicyUpdate(Schema):
    ttl_minutes_by_role: Dict[str, int]

class BruteforcePolicyUpdate(Schema):
    max_failed_attempts: int
    lock_minutes: int
