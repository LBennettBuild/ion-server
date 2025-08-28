from ..models import User, Role, UserRole
from django.db import transaction
from typing import List

# ---------------- Roles ----------------
def list_roles(tenant_id: str):
    return Role.objects.filter(tenant_id=tenant_id)

def get_role(role_id: str):
    return Role.objects.get(id=role_id)

def create_role(tenant_id: str, data: dict):
    role = Role.objects.create(tenant_id=tenant_id, **data)
    return role

def update_role(role_id: str, data: dict):
    role = Role.objects.get(id=role_id)
    for field, value in data.items():
        if value is not None:
            setattr(role, field, value)
    role.save()
    return role

def delete_role(role_id: str):
    role = Role.objects.get(id=role_id)
    role.delete()
    return True

# ---------------- Users ----------------
def list_users(tenant_id: str, filters: dict = None):
    qs = User.objects.filter(tenant_id=tenant_id)
    if filters:
        qs = qs.filter(**filters)
    return qs

def get_user(user_id: str):
    return User.objects.get(id=user_id)

@transaction.atomic
def create_user(tenant_id: str, data: dict):
    roles = data.pop("roles", [])
    user = User.objects.create(tenant_id=tenant_id, **data)
    for role_id in roles:
        UserRole.objects.create(user=user, role_id=role_id)
    return user

@transaction.atomic
def update_user(user_id: str, data: dict):
    roles = data.pop("roles", None)
    user = User.objects.get(id=user_id)
    for field, value in data.items():
        if value is not None:
            setattr(user, field, value)
    user.save()
    if roles is not None:
        # replace roles
        UserRole.objects.filter(user=user).delete()
        for role_id in roles:
            UserRole.objects.create(user=user, role_id=role_id)
    return user

def deactivate_user(user_id: str):
    user = User.objects.get(id=user_id)
    user.status = "inactive"
    user.save()
    return user

def activate_user(user_id: str):
    user = User.objects.get(id=user_id)
    user.status = "active"
    user.save()
    return user

def delete_user(user_id: str):
    """
    Delete a single user by ID
    """
    User.objects.filter(id=user_id).delete()
    return True

@transaction.atomic
def bulk_create_users(tenant_id: str, users_data: list):
    """
    Create multiple users in bulk.
    `users_data` is a list of dicts, each containing user fields and optional 'roles'.
    """
    created_users = []
    for data in users_data:
        roles = data.pop("roles", [])
        user = User.objects.create(tenant_id=tenant_id, **data)
        for role_id in roles:
            UserRole.objects.create(user=user, role_id=role_id)
        created_users.append(user)
    return created_users

# ---------------- IAM helper ----------------
@transaction.atomic
def assign_roles_to_user(user_id: str, add_roles: List[str] = None, remove_roles: List[str] = None):
    user = User.objects.get(id=user_id)
    add_roles = add_roles or []
    remove_roles = remove_roles or []

    # Remove roles
    if remove_roles:
        UserRole.objects.filter(user=user, role_id__in=remove_roles).delete()

    # Add roles
    for role_id in add_roles:
        UserRole.objects.get_or_create(user=user, role_id=role_id)

    return user
