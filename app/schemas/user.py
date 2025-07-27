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
    """
    Schema representing a user with non-sensitive information.
    Attributes:
        id (int): Unique identifier of the user.
        username (str): Username of the user.
        email (str): Email address of the user.
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        is_active (bool): Indicates whether the user account is active.
        date_joined (str): Date when the user joined, in ISO format.
        birth_date (str): User's birth date, in ISO format.
    """
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
