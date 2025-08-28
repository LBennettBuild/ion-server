import uuid
from ..models import Tenant, User, Role, Session, BackupCode
from ..utils.jwt import issue_access, issue_refresh
from django.utils import timezone

# ----------------------
# Registration
# ----------------------
def register_owner(data, lang: str):
    owner_data = data["owner"]

    if User.objects.filter(email=owner_data["email"]).exists():
        raise ValueError("User with this email already exists")

    tenant = Tenant.objects.create(
        company_name=data["company_name"],
        inn=data["inn"],
        activity_type=data["activity_type"],
        settings_security={}
    )

    user = User.objects.create(
        tenant=tenant,
        email=owner_data["email"],
        first_name=owner_data["first_name"],
        last_name=owner_data["last_name"],
        phone=owner_data.get("phone"),
        password_hash=owner_data["password"],  # TODO: hash in production
    )

    role, _ = Role.objects.get_or_create(
        tenant=None, name="business_owner", system=True
    )
    user.user_roles.create(role=role)

    return {
        "tenant_id": str(tenant.id),
        "user_id": str(user.id),
        "email_verification_required": True
    }


# ----------------------
# Login & MFA
# ----------------------
def login(email: str, password: str, device_fp: str, lang: str):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return {"error": "Invalid credentials"}

    # TODO: check password hash
    mfa_required = True
    if mfa_required:
        intermediate = str(uuid.uuid4())
        # TODO: send OTP to email
        return {
            "mfa_required": True,
            "mfa_methods": ["email_otp"],
            "intermediate_token": intermediate
        }

    # Issue JWT tokens
    access = issue_access(sub=str(user.id), tid=str(user.tenant.id), roles=["business_owner"], perms=["*"], sid="sess01", device_id=device_fp or "dev")
    refresh = issue_refresh(sub=str(user.id), tid=str(user.tenant.id), sid="sess01", device_id=device_fp or "dev")
    return {
        "access_token": access,
        "refresh_token": refresh,
        "expires_in": 900,
        "remember_device_cookie": True
    }


# ----------------------
# MFA verify
# ----------------------
def verify_email_otp(intermediate: str, code: str, remember_device: bool, device_fp: str):
    # TODO: verify OTP
    access = issue_access(sub="user_id", tid="tenant_id", roles=["business_owner"], perms=["*"], sid="sess01", device_id=device_fp or "dev")
    refresh = issue_refresh(sub="user_id", tid="tenant_id", sid="sess01", device_id=device_fp or "dev")
    return {
        "access_token": access,
        "refresh_token": refresh,
        "expires_in": 900,
        "remember_device_cookie": remember_device
    }


# ----------------------
# Logout
# ----------------------
def logout(user_id: str, all_devices: bool, current_sid: str):
    # TODO: invalidate session(s)
    return {"ok": True}


# ----------------------
# Token refresh
# ----------------------
def refresh_tokens(refresh_token: str, device_fp: str):
    access = issue_access(sub="user_id", tid="tenant_id", roles=["business_owner"], perms=["*"], sid="sess01", device_id=device_fp or "dev")
    new_refresh = issue_refresh(sub="user_id", tid="tenant_id", sid="sess01", device_id=device_fp or "dev")
    return {
        "access_token": access,
        "refresh_token": new_refresh,
        "expires_in": 900,
        "remember_device_cookie": True
    }


# ----------------------
# Backup codes
# ----------------------
def generate_backup_codes(user_id: str):
    codes = ["AB12-CD34", "EF56-GH78"]
    # TODO: save hashed codes
    return {"codes": codes}

def list_backup_codes_masked(user_id: str):
    codes = ["****-CD34", "****-GH78"]
    return {"codes": codes}
