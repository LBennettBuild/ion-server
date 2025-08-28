# server/admin.py
from django.contrib import admin
from .models import (
    Tenant, User, Role, UserRole, Session,
    AuditLog, OAuthClient, ApiKey, BackupCode
)

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_name', 'inn', 'activity_type', 'created_at')
    search_fields = ('company_name', 'inn')
    list_filter = ('activity_type',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'tenant', 'status', 'email_verified_at')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('status', 'tenant')


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'tenant', 'system')
    search_fields = ('name',)
    list_filter = ('system', 'tenant')


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'role')
    search_fields = ('user__email', 'role__name')


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tenant', 'device_id', 'ip', 'created_at', 'last_seen', 'trusted_until')
    search_fields = ('user__email', 'device_id', 'ip')
    list_filter = ('tenant',)


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'tenant', 'user', 'event', 'ip', 'ua', 'at')
    search_fields = ('event', 'user__email', 'ip')
    list_filter = ('tenant', 'event')


@admin.register(OAuthClient)
class OAuthClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'tenant', 'type')
    search_fields = ('name',)
    list_filter = ('type', 'tenant')


@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'tenant', 'created_at', 'revoked_at')
    search_fields = ('name',)
    list_filter = ('tenant',)


@admin.register(BackupCode)
class BackupCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'code_hash', 'used_at')
    search_fields = ('user__email',)
