from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from sqlalchemy.orm import Session as SQLSession

from app.config.database import get_db
from app.schemas.user import SensitiveUserSchema, NonSensitiveUserSchema, UserRegisterSchema, UserLoginSchema
from app.controller.users import add_new_user, query_users, login

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/add-user", tags=["Users"], response_model=SensitiveUserSchema, description="Add a new user")
async def new_user(user: SensitiveUserSchema):
    response = add_new_user(user)
    return response

@router.get("/get-user/{user_id}", tags=["Users"], response_model=NonSensitiveUserSchema | SensitiveUserSchema, description="Get a user by ID")
async def get_user(user_id: int):
    response = query_users(id=user_id)
    if not response:
        raise HTTPException(status_code=404, detail="User not found")
    return response

@router.get("/get-user", tags=["Users"], response_model=list[NonSensitiveUserSchema], description="Get all users")
async def get_all_users():
    response = query_users()
    if not response:
        raise HTTPException(status_code=404, detail="User not found")
    return response

@router.post("/register", tags=["Users"], description="Register a new user")
async def register_user(user: UserRegisterSchema):
    try:
        response = add_new_user(user)
        return response
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login", tags=["Users"], description="Login a user")
async def login_user(user: OAuth2PasswordRequestForm = Depends(), db: SQLSession = Depends(get_db)):
    try:
        response = login(user, db)
        return response
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tokenvalidate", tags=["Users"], description="Validate a token")
async def validate_token(token: str):
    try:
        response = token_validator(token)
        return response
    except JWTError:
        return {"status": "invalid"}