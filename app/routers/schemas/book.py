from pydantic import BaseModel

class BookSchema(BaseModel):
    title: str
    author: str
    published_year: int | None
    isbn: str | None
    pages: int | None
    cover: str | None
    language: str | None

    class Config:
        orm_mode = True
        from_attributes=True
      

class ReturnBookSchema(BaseModel):
    id: int
    title: str
    author: str
    published_year: int | None
    isbn: str | None
    pages: int | None
    cover: str | None
    language: str | None

    class Config:
        orm_mode = True
        from_attributes=True
      
