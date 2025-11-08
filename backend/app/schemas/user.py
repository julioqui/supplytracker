from pydantic import BaseModel, EmailStr
from typing import List, Optional
from uuid import UUID
from datetime import datetime


class TenantBase(BaseModel):
    name: str
    domain: Optional[str] = None


class TenantResponse(TenantBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class RoleBase(BaseModel):
    name: str


class RoleResponse(RoleBase):
    id: int
    tenant_id: UUID

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: EmailStr


class UserResponse(UserBase):
    id: str
    tenant_id: UUID
    is_active: bool
    roles: List[RoleResponse] = []

    class Config:
        from_attributes = True
