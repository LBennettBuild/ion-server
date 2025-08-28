from ninja import Router
from typing import List
from ..schemas.roles import RoleOut, RoleCreate, RoleUpdate, AssignRolesSchema
from ..schemas.users import UserOut, UserCreate, UserUpdate, UsersFilter, BulkUsers
from ..services.iam import (
    list_roles, create_role, update_role, delete_role, assign_roles_to_user,
    list_users, create_user, update_user, delete_user, bulk_create_users
)

router = Router()

# ----------------------
# Roles
# ----------------------
@router.get("/iam/roles", response=List[RoleOut])
def get_roles(request, tenant_id: str):
    roles = list_roles(tenant_id)
    return [RoleOut(
        id=str(r.id),
        name=r.name,
        system=r.system,
        inherits=r.inherits,
        permissions=r.permissions
    ) for r in roles]

@router.post("/iam/roles", response=RoleOut)
def create_role_endpoint(request, tenant_id: str, data: RoleCreate):
    role = create_role(tenant_id, data.dict())
    return RoleOut(
        id=str(role.id),
        name=role.name,
        system=role.system,
        inherits=role.inherits,
        permissions=role.permissions
    )

@router.put("/iam/roles/{role_id}", response=RoleOut)
def update_role_endpoint(request, role_id: str, data: RoleUpdate):
    role = update_role(role_id, data.dict(exclude_none=True))
    return RoleOut(
        id=str(role.id),
        name=role.name,
        system=role.system,
        inherits=role.inherits,
        permissions=role.permissions
    )

@router.delete("/iam/roles/{role_id}", response=dict)
def delete_role_endpoint(request, role_id: str):
    delete_role(role_id)
    return {"detail": "Role deleted"}

@router.post("/iam/users/{user_id}/roles", response=dict)
def assign_roles_endpoint(request, user_id: str, data: AssignRolesSchema):
    assign_roles_to_user(user_id, add_roles=data.add, remove_roles=data.remove)
    return {"detail": "Roles updated"}

# ----------------------
# Users
# ----------------------
@router.get("/iam/users", response=List[UserOut])
def get_users(request, tenant_id: str, filters: UsersFilter = UsersFilter()):
    users = list_users(tenant_id, filters.dict(exclude_none=True))
    return [UserOut(
        id=str(u.id),
        full_name=f"{u.first_name} {u.last_name}",
        email=u.email,
        position=u.position,
        department=u.department,
        status=u.status,
        roles=[ur.role.name for ur in u.user_roles.all()]
    ) for u in users]

@router.post("/iam/users", response=UserOut)
def create_user_endpoint(request, tenant_id: str, data: UserCreate):
    user = create_user(tenant_id, data.dict())
    return UserOut(
        id=str(user.id),
        full_name=f"{user.first_name} {user.last_name}",
        email=user.email,
        position=user.position,
        department=user.department,
        status=user.status,
        roles=[ur.role.name for ur in user.user_roles.all()]
    )

@router.put("/iam/users/{user_id}", response=UserOut)
def update_user_endpoint(request, user_id: str, data: UserUpdate):
    user = update_user(user_id, data.dict(exclude_none=True))
    return UserOut(
        id=str(user.id),
        full_name=f"{user.first_name} {user.last_name}",
        email=user.email,
        position=user.position,
        department=user.department,
        status=user.status,
        roles=[ur.role.name for ur in user.user_roles.all()]
    )

@router.delete("/iam/users/{user_id}", response=dict)
def delete_user_endpoint(request, user_id: str):
    delete_user(user_id)
    return {"detail": "User deleted"}

@router.post("/iam/users/bulk", response=List[UserOut])
def bulk_create_users_endpoint(request, tenant_id: str, data: BulkUsers):
    users = bulk_create_users(tenant_id, [u.dict() for u in data.users])
    return [UserOut(
        id=str(u.id),
        full_name=f"{u.first_name} {u.last_name}",
        email=u.email,
        position=u.position,
        department=u.department,
        status=u.status,
        roles=[ur.role.name for ur in u.user_roles.all()]
    ) for u in users]
