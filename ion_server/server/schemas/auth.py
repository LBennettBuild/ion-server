from ninja import Schema
from typing import List, Optional

# ----------------------
# Owner & Registration
# ----------------------
class OwnerSchema(Schema):
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    password: str

class RegisterOwnerSchema(Schema):
    company_name: str
    inn: str
    activity_type: str
    owner: OwnerSchema

class RegisterOwnerOut(Schema):
    tenant_id: str
    user_id: str
    email_verification_required: bool

# ----------------------
# Email verification
# ----------------------
class ResendEmailSchema(Schema):
    email: str

class ConfirmEmailSchema(Schema):
    token: str

# ----------------------
# Login & MFA
# ----------------------
class LoginSchema(Schema):
    email: str
    password: str
    device_fingerprint: Optional[str] = None

class LoginMFAOut(Schema):
    mfa_required: bool
    mfa_methods: List[str]
    intermediate_token: str

class LoginSuccessOut(Schema):
    access_token: str
    refresh_token: str
    expires_in: int
    remember_device_cookie: bool

class VerifyEmailMFASchema(Schema):
    intermediate_token: str
    code: str
    remember_device: bool = True

# ----------------------
# Tokens
# ----------------------
class RefreshSchema(Schema):
    refresh_token: str
    device_fingerprint: Optional[str] = None

# ----------------------
# Logout
# ----------------------
class LogoutSchema(Schema):
    all_devices: bool = False

# ----------------------
# Backup codes
# ----------------------
class BackupCodesOut(Schema):
    codes: List[str]

class MaskedBackupCodesOut(Schema):
    codes: List[str]

class ErrorOut(Schema):
    error: str