from ninja import Router
from typing import Optional
from typing import Union
from ..schemas.auth import *
from ..services.auth import (
    register_owner,
    login,
    verify_email_otp,
    logout,
    refresh_tokens,
    generate_backup_codes,
    list_backup_codes_masked
)

router = Router()

# ----------------------
# Registration
# ----------------------
@router.post("/auth/register-owner", response={201: RegisterOwnerOut, 400: ErrorOut})
def register_owner_endpoint(request, data: RegisterOwnerSchema):
    try:
        result = register_owner(data.dict(), lang=request.headers.get("Accept-Language", "uz"))
        return 201, result
    except Exception as e:
        return 400, {"error": str(e)}


# ----------------------
# Login
# ----------------------
@router.post("/auth/login", response={200: Union[LoginMFAOut, LoginSuccessOut]})
def login_endpoint(request, data: LoginSchema):
    lang = request.headers.get("Accept-Language", "uz")
    result = login(data.email, data.password, data.device_fingerprint, lang=lang)

    if result.get("mfa_required"):
        return LoginMFAOut(**result)
    return LoginSuccessOut(**result)

# ----------------------
# MFA verify
# ----------------------
@router.post("/auth/mfa/email/verify", response={200: LoginSuccessOut, 400: ErrorOut})
def mfa_verify_endpoint(request, data: VerifyEmailMFASchema):
    try:
        result = verify_email_otp(
            intermediate=data.intermediate_token,
            code=data.code,
            remember_device=data.remember_device,
            device_fp=None
        )
        return LoginSuccessOut(**result)
    except Exception as e:
        return 400, {"error": str(e)}


# ----------------------
# Logout
# ----------------------
@router.post("/auth/logout", response={200: dict, 400: ErrorOut})
def logout_endpoint(request, data: LogoutSchema):
    try:
        result = logout(user_id="stub", all_devices=data.all_devices, current_sid="sess01")
        return result
    except Exception as e:
        return 400, {"error": str(e)}


# ----------------------
# Refresh tokens
# ----------------------
@router.post("/auth/token/refresh", response={200: LoginSuccessOut, 400: ErrorOut})
def refresh_endpoint(request, data: RefreshSchema):
    try:
        result = refresh_tokens(data.refresh_token, data.device_fingerprint)
        return LoginSuccessOut(**result)
    except Exception as e:
        return 400, {"error": str(e)}


# ----------------------
# Backup codes
# ----------------------
@router.post("/auth/mfa/backup-codes/generate", response={200: BackupCodesOut, 400: ErrorOut})
def backup_generate_endpoint(request):
    try:
        result = generate_backup_codes(user_id="stub")
        return BackupCodesOut(**result)
    except Exception as e:
        return 400, {"error": str(e)}


@router.get("/auth/mfa/backup-codes", response={200: MaskedBackupCodesOut, 400: ErrorOut})
def backup_list_endpoint(request):
    try:
        result = list_backup_codes_masked(user_id="stub")
        return MaskedBackupCodesOut(**result)
    except Exception as e:
        return 400, {"error": str(e)}
