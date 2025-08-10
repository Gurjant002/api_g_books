import re
from datetime import datetime, timedelta
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from app.config.database import get_db, db_transaction
from app.config.authentication import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.schemas.token import Token
from app.schemas.user import NonSensitiveUserSchema, SensitiveUserSchema, UserRegisterSchema
from app.models.users import User as UserModel

class UserService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.email_regex = r"^([a-z]|[0-9]|\-|\_|\+|\.)+\@([a-z]|[0-9]){2,}\.[a-z]{2,}(\.[a-z]{2,})?$"
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def login(self, user: OAuth2PasswordRequestForm) -> NonSensitiveUserSchema:
        if user.username is None or user.password is None:
            raise HTTPException(status_code=400, detail="Username and password are required")

        db_user = None
        with get_db() as db:
            if re.match(self.email_regex, user.username) is None:
                db_user = db.query(UserModel).filter(UserModel.username == user.username).first()
            else:
                db_user = db.query(UserModel).filter(UserModel.email == user.username).first()

        if not db_user or not self.verify_password(user.password, db_user.password):
            raise HTTPException(status_code=401, detail="Invalid username or password")
        
        token: Token = Token(
            access_token=self.create_access_token(data={"sub": db_user.id}),
            tocken_expiration=str(datetime.utcnow() + timedelta(minutes=30)),
            token_type="bearer"
        )
    
    def add_new_user(self, user: SensitiveUserSchema | UserRegisterSchema) -> NonSensitiveUserSchema:
        with db_transaction() as db:
            if isinstance(user, UserRegisterSchema):
                if re.match(self.email_regex, user.email) is None:
                    raise HTTPException(status_code=400, detail="Invalid email address")
                
                if db.query(UserModel).filter(UserModel.username == user.username).first():
                    raise HTTPException(status_code=400, detail="Username already exists")
                
                if db.query(UserModel).filter(UserModel.email == user.email).first():
                    raise HTTPException(status_code=400, detail="Email already registered")
            
                if len(user.password) < 8:
                    raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")

            new_user = UserModel(**user.dict())
            db.add(new_user)
            db.refresh(new_user) # This can fail
            return NonSensitiveUserSchema.from_orm(new_user)
