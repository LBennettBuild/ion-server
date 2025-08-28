from ninja import Schema
from typing import List, Optional

class PermissionOut(Schema):
    key: str
    description: str

class RoleOut(Schema):
    id: str
    name: str
    system: bool
    inherits: List[str]
    permissions: List[str]

class RoleCreate(Schema):
    name: str
    inherits: Optional[List[str]] = []
    permissions: Optional[List[str]] = []

class RoleUpdate(Schema):
    name: Optional[str] = None
    inherits: Optional[List[str]] = None
    permissions: Optional[List[str]] = None

class AssignRolesSchema(Schema):
    add: Optional[List[str]] = []
    remove: Optional[List[str]] = []
