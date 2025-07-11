import re
from datetime import datetime, timedelta
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt

from app.config.authentication import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.models.users import User as UserModel
from app.config.database import Session
from app.schemas.user import SensitiveUserSchema, NonSensitiveUserSchema, UserRegisterSchema, UserLoginSchema
from app.schemas.token import Token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
email_regex = r"^([a-z]|[0-9]|\-|\_|\+|\.)+\@([a-z]|[0-9]){2,}\.[a-z]{2,}(\.[a-z]{2,})?$"

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def add_new_user(user: SensitiveUserSchema | UserRegisterSchema ) -> NonSensitiveUserSchema:
    db = Session()
    if isinstance(user, UserRegisterSchema):
        if re.match(email_regex, user.email) is None:
            db.close()
            raise HTTPException(status_code=400, detail="Invalid email address")
        
        if db.query(UserModel).filter(UserModel.email == user.email).first():
            db.close()
            raise HTTPException(status_code=400, detail="Email already exists")

        if len(user.password) < 8:
            db.close()
            raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")
        
        if user.password != user.confirm_password:
            db.close()
            raise HTTPException(status_code=400, detail="Passwords do not match")

        if db.query(UserModel).filter(UserModel.username == user.username).first():
            db.close()
            raise HTTPException(status_code=400, detail="Username already exists")

    user.password = pwd_context.hash(user.password)

    """ 
     Este fragmento de código se encarga de crear una nueva instancia del modelo de usuario (UserModel) utilizando los datos proporcionados por el objeto user. Primero, verifica si el atributo confirm_password del usuario no está presente o es falso. Si es así, utiliza todos los campos del usuario para crear el nuevo usuario. En cambio, si confirm_password está presente, excluye ese campo al crear el nuevo usuario.

     Esto es útil porque el campo confirm_password generalmente se utiliza solo para validar que el usuario haya escrito correctamente su contraseña durante el registro, pero no debe almacenarse en la base de datos. Así, el código garantiza que solo los datos necesarios y seguros se guarden en el modelo de usuario.
     """
    if not user.confirm_password:
        new_user = UserModel(**user.model_dump())
    else:
        new_user = UserModel(**user.model_dump(exclude={"confirm_password"}))

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    response = SensitiveUserSchema.from_orm(new_user)
    return response

def login(user: OAuth2PasswordRequestForm, db: Session) -> NonSensitiveUserSchema:
    # db = Session()
    if user.username is None:
        db.close()
        raise HTTPException(status_code=400, detail="Username or email must be provided")
    
    db_user = db.query(UserModel).filter(UserModel.email == user.username).first()
    if not db_user:
        db_user = db.query(UserModel).filter(UserModel.username == user.username).first()

    if not db_user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")

    if not db_user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(user.password, db_user.password):
        db.close()
        raise HTTPException(status_code=400, detail="Invalid password")

    token: Token = Token(
        access_token=create_access_token(data={"sub": db_user.email}),
        tocken_expiration=str(datetime.utcnow() + timedelta(minutes=30)),
        token_type="bearer"
    )
    return token

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

def token_validator(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"status": "valid", "payload": payload}
    except JWTError:
        return {"status": "invalid"}
