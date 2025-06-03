from pydantic import BaseModel

from app.schemas.UserSchema import UserCreate, UserResponse


class AdminBase(BaseModel):
    pass


class AdminCreate(AdminBase):
    user: UserCreate


class AdminUpdate(BaseModel):
    pass


class AdminResponse(AdminBase):
    admin_id: int
    user_id: int
    user: UserResponse

    class Config:
        from_attributes = True
