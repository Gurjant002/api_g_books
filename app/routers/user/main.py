from fastapi import APIRouter, HTTPException
from app.routers.schemas.user import SensitiveUserSchema, NonSensitiveUserSchema
from app.controller.users import add_new_user, query_users

router = APIRouter()

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
