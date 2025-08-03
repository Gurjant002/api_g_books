from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from sqlalchemy.orm import Session as SQLSession

from app.config.database import get_db
from app.schemas.user import SensitiveUserSchema, NonSensitiveUserSchema, UserRegisterSchema, UserLoginSchema
from app.controller.users import add_new_user, query_users, login, token_validator, oauth2_scheme, get_current_user

router = APIRouter()

@router.post("/add-user", tags=["Users"], response_model=SensitiveUserSchema, description="Add a new user")
async def new_user(user: SensitiveUserSchema):
    response = add_new_user(user)
    return response

@router.get("/get-user/{user_id}", tags=["Users"], response_model=NonSensitiveUserSchema | SensitiveUserSchema, description="Get a user by ID")
async def get_user(user_id: int, token: str = Depends(oauth2_scheme)):
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    if not token:
        raise HTTPException(status_code=401, detail="Token is required")
    validation = query_users(token=token)
    if validation.id != user_id:
        raise HTTPException(status_code=403, detail="You do not have permission to access this user")
    response = query_users(id=user_id)
    if not response:
        raise HTTPException(status_code=404, detail="User not found")
    return response

@router.get("/get-profile", tags=["Users"], response_model=NonSensitiveUserSchema, description="Get user profile")
async def get_profile(current_user: NonSensitiveUserSchema = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    return current_user

@router.get("/get-user", tags=["Users"], response_model=list[NonSensitiveUserSchema], description="Get all users")
async def get_all_users():
    response = query_users()
    if not response:
        raise HTTPException(status_code=404, detail="User not found")
    return response

@router.get("/get-user-by-email", tags=["Users"], response_model=NonSensitiveUserSchema, description="Get a user by email")
async def get_user_by_email(email: str):
    response = query_users(email=email)
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

@router.get("/validate-token", tags=["Users"], description="Validate a token")
async def validate_token(token: str = Depends(oauth2_scheme)):
    try:
        response = query_users(token=token)
        return response
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tokenvalidate", tags=["Users"], description="Validate a token")
async def validate_token(token: str = Depends(oauth2_scheme)):
    try:
        response = token_validator(token)
        return response
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))