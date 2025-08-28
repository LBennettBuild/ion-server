def ok(data=None, status=200):
    return status, {"ok": True, "data": data}

def fail(code: str, message: str, status=400, details=None):
    return status, {"ok": False, "error": {"code": code, "message": message, "details": details}}
