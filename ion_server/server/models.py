from django.db import models


# Create your models here.
class Tenant(models.Model):
    company_name = models.CharField(max_length=255)
    inn = models.CharField(max_length=20)
    activity_type = models.CharField(max_length=100)
    settings_security = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)


class User(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='users')
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password_hash = models.CharField(max_length=255)
    position = models.CharField(max_length=100, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=50, default='active')
    email_verified_at = models.DateTimeField(null=True, blank=True)


class Role(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, blank=True, related_name='roles')
    name = models.CharField(max_length=100)
    system = models.BooleanField(default=False)
    inherits = models.JSONField(default=list)
    permissions = models.JSONField(default=list)


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_roles')


class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='sessions')
    device_id = models.CharField(max_length=255)
    ip = models.GenericIPAddressField()
    ua = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)
    trusted_until = models.DateTimeField(null=True, blank=True)


class AuditLog(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='audit_logs')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs')
    event = models.CharField(max_length=100)
    data = models.JSONField(default=dict)
    ip = models.GenericIPAddressField()
    ua = models.TextField()
    at = models.DateTimeField(auto_now_add=True)


class OAuthClient(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, blank=True, related_name='oauth_clients')
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    redirect_uris = models.JSONField(default=list)
    scopes = models.JSONField(default=list)


class ApiKey(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='api_keys')
    name = models.CharField(max_length=255)
    key_hash = models.CharField(max_length=255)
    scopes = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    revoked_at = models.DateTimeField(null=True, blank=True)


class BackupCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='backup_codes')
    code_hash = models.CharField(max_length=255)
    used_at = models.DateTimeField(null=True, blank=True)
