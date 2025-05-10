from fastapi import HTTPException
from app.models.users import User as UserModel
from app.schemas.user import SensitiveUserSchema, NonSensitiveUserSchema, UserRegisterSchema, UserLoginSchema
from app.config.database import Session
import re

email_regex = r"^([a-z]|[0-9]|\-|\_|\+|\.)+\@([a-z]|[0-9]){2,}\.[a-z]{2,}(\.[a-z]{2,})?$"

def add_new_user(user: SensitiveUserSchema | UserRegisterSchema ) -> NonSensitiveUserSchema:
    db = Session()
    if isinstance(user, UserRegisterSchema):
        if re.match(email_regex, user.email) is None:
            raise HTTPException(status_code=400, detail="Invalid email address")
        
        if db.query(UserModel).filter(UserModel.email == user.email).first():
            raise HTTPException(status_code=400, detail="Email already exists")

        if len(user.password) < 8:
            raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")
        
        if user.password != user.password_confirm:
            raise HTTPException(status_code=400, detail="Passwords do not match")

        if db.query(UserModel).filter(UserModel.username == user.username).first():
            raise HTTPException(status_code=400, detail="Username already exists")

    if not user.password_confirm:
        new_user = UserModel(**user.model_dump())
    else:
        new_user = UserModel(**user.model_dump(exclude={"password_confirm"}))

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    response = SensitiveUserSchema.from_orm(new_user)
    return response

def login(user: UserLoginSchema) -> NonSensitiveUserSchema:
    db = Session()
    if user.email is None or user.username is None:
        raise HTTPException(status_code=400, detail="Username or email must be provided")
    
    else:
        db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
        if not db_user:
            db_user = db.query(UserModel).filter(UserModel.username == user.username).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db.close()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.password != user.password:
        raise HTTPException(status_code=400, detail="Invalid password")

    response = NonSensitiveUserSchema.from_orm(db_user)
    return response

def query_users(id: int = None, sensitive: bool = False) -> list[NonSensitiveUserSchema] | list[SensitiveUserSchema] | NonSensitiveUserSchema | SensitiveUserSchema:
    db = Session()
    if id is not None:
        user = db.query(UserModel).filter(UserModel.id == id).first()
        db.close()
        if not user:
            return None
        if not sensitive:
            response = NonSensitiveUserSchema.from_orm(user)
        else:
            response = SensitiveUserSchema.from_orm(user)
        return response
    users = db.query(UserModel).all()
    db.close()
    if not sensitive:
        response = [NonSensitiveUserSchema.from_orm(user) for user in users]
    else:
        response = [SensitiveUserSchema.from_orm(user) for user in users]
    return response
