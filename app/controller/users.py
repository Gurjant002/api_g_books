from app.models.users import User as UserModel
from app.schemas.user import SensitiveUserSchema, NonSensitiveUserSchema
from app.config.database import Session

def add_new_user(user: SensitiveUserSchema) -> NonSensitiveUserSchema:
    db = Session()
    new_user = UserModel(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    response = SensitiveUserSchema.from_orm(new_user)
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
