from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    tocken_expiration: str
    token_type: str