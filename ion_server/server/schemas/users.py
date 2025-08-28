from ninja import Schema
from typing import List, Optional

class UserOut(Schema):
    id: str
    full_name: str
    email: str
    position: Optional[str] = None
    department: Optional[str] = None
    status: str
    roles: List[str]

class UserCreate(Schema):
    full_name: str
    email: str
    position: Optional[str] = None
    department: Optional[str] = None
    roles: Optional[List[str]] = []

class UserUpdate(Schema):
    full_name: Optional[str] = None
    position: Optional[str] = None
    department: Optional[str] = None
    roles: Optional[List[str]] = None
    status: Optional[str] = None

class UsersFilter(Schema):
    department: Optional[str] = None
    roles: Optional[List[str]] = None
    status: Optional[str] = None
    q: Optional[str] = None

class BulkUsers(Schema):
    users: List[UserCreate]
