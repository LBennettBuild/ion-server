from ..models import Session, AuditLog, Tenant
from django.utils import timezone
from datetime import timedelta

# Sessions
def list_sessions(tenant_id: str, user_id: str = None):
    query = Session.objects.filter(tenant_id=tenant_id)
    if user_id:
        query = query.filter(user_id=user_id)
    return [
        {
            "session_id": str(s.id),
            "user_id": str(s.user_id),
            "ip": s.ip,
            "ua": s.ua,
            "created_at": s.created_at.isoformat(),
            "last_seen": s.last_seen.isoformat(),
            "device_trusted": bool(s.trusted_until and s.trusted_until > timezone.now())
        }
        for s in query
    ]


def revoke_session(session_id: str):
    Session.objects.filter(id=session_id).delete()
    return True


# Audit logs
def list_audit_logs(tenant_id: str, filters: dict = None):
    query = AuditLog.objects.filter(tenant_id=tenant_id)
    if filters:
        if filters.get("user_id"):
            query = query.filter(user_id=filters["user_id"])
        if filters.get("event"):
            query = query.filter(event=filters["event"])
        if filters.get("ip"):
            query = query.filter(ip=filters["ip"])
        if filters.get("date_from"):
            query = query.filter(at__gte=filters["date_from"])
        if filters.get("date_to"):
            query = query.filter(at__lte=filters["date_to"])
    return [
        {
            "id": str(a.id),
            "user_id": str(a.user_id) if a.user_id else None,
            "event": a.event,
            "data": a.data,
            "ip": a.ip,
            "ua": a.ua,
            "at": a.at.isoformat()
        } for a in query
    ]


# Security policies
def update_session_policy(tenant_id: str, policy: dict):
    tenant = Tenant.objects.get(id=tenant_id)
    tenant.settings_security["session"] = policy
    tenant.save()
    return tenant.settings_security["session"]


def update_bruteforce_policy(tenant_id: str, policy: dict):
    tenant = Tenant.objects.get(id=tenant_id)
    tenant.settings_security["bruteforce"] = policy
    tenant.save()
    return tenant.settings_security["bruteforce"]
