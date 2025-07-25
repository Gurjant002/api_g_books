from pydantic import BaseModel
from app.schemas.book import BookSchemaWithOwner

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
    first_name: str
    last_name: str
    is_active: bool
    date_joined: str
    birth_date: str

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

class UserBookSchema(BaseModel):
    user: NonSensitiveUserSchema
    readed_books: list[BookSchemaWithOwner]
    rented_books: list[BookSchemaWithOwner]

    class Config:
        # orm_mode = True
        from_attributes=True