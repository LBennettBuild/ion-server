from ninja import Router
from typing import List, Optional
from ..schemas.security import (
    SessionOut,
    AuditLogOut,
    AuditFilter,
    SessionPolicyUpdate,
    BruteforcePolicyUpdate
)
from ..services.security import (
    list_sessions,
    list_audit_logs,
    update_session_policy,
    update_bruteforce_policy
)

router = Router()

# ----------------------
# Sessions
# ----------------------
@router.get("/security/sessions", response=List[SessionOut])
def get_sessions(request):
    sessions = list_sessions()  # returns list of dicts matching SessionOut
    return [SessionOut(**s) for s in sessions]

# ----------------------
# Audit Logs
# ----------------------
@router.get("/security/audit-logs", response=List[AuditLogOut])
def get_audit_logs(request, filters: Optional[AuditFilter] = None):
    logs = list_audit_logs(filters.dict() if filters else {})
    return [AuditLogOut(**log) for log in logs]

# ----------------------
# Session Policy
# ----------------------
@router.put("/security/session-policy", response=dict)
def update_session_policy_endpoint(request, data: SessionPolicyUpdate):
    result = update_session_policy(data.dict())
    return result

# ----------------------
# Bruteforce Policy
# ----------------------
@router.put("/security/bruteforce-policy", response=dict)
def update_bruteforce_policy_endpoint(request, data: BruteforcePolicyUpdate):
    result = update_bruteforce_policy(data.dict())
    return result
