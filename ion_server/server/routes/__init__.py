from ninja import NinjaAPI
from .auth import router as auth_router
from .tenant import router as tenant_router
from .iam import router as iam_router
from .security import router as security_router
from .oauth import router as oauth_router

api_router = NinjaAPI(
    title="ION ERP API",
)

api_router.add_router("/auth/", auth_router,tags=["Auth"])
api_router.add_router("/tenant/", tenant_router,tags=["Tenant"])
api_router.add_router("/iam/", iam_router,tags=["IAM"])
api_router.add_router("/security/", security_router,tags=["Security"])
api_router.add_router("/oauth2/", oauth_router,tags=["OAuth2"])

__all__ = ["api_router"]
