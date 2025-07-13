from pydantic import BaseModel

class SensitiveUserSchema(BaseModel):
    id: int
    username: str
    email: str
    password: str
    first_name: str | None
    last_name: str | None
    is_active: bool
    is_superuser: bool
    is_verified: bool
    date_joined: str | None
    birth_date: str | None

    class Config:
        # orm_mode = True
        from_attributes=True

class NonSensitiveUserSchema(BaseModel):
    id: int
    username: str
    email: str
    first_name: str | None
    last_name: str | None
    is_active: bool

    class Config:
        # orm_mode = True
        from_attributes=True

class UserRegisterSchema(BaseModel):
    username: str
    email: str
    password: str
    confirm_password: str
    first_name: str | None
    last_name: str | None
    date_joined: str | None
    birth_date: str | None

    class Config:
        # orm_mode = True
        from_attributes=True

class UserLoginSchema(BaseModel):
    username: str | None
    email: str | None
    password: str
