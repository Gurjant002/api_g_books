from pydantic import BaseModel

class BookSchema(BaseModel):
    title: str
    author: str
    published_year: int | None
    isbn: str | None
    pages: int | None
    cover: str | None
    language: str | None
    available: bool = True  # Default to True for availability
    owner_id: int | None = None  # Optional owner ID for book ownership
    date_added: str | None = None  # Optional date added for the book

    class Config:
        # orm_mode = True
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
    available: bool | None   # Default to True for availability
    owner_id: int | None = None  # Optional owner ID for book ownership
    date_added: str | None = None  # Optional date added for the book

    class Config:
        # orm_mode = True
        from_attributes=True

class ReadedBookSchema(BaseModel):
    book_id: int
    user_id: int
    start: str | None = None  # Optional start date in ISO format
    end: str | None = None  # Optional end date in ISO format

    class Config:
        # orm_mode = True
        from_attributes=True

class RentedBookSchema(BaseModel):
    book_id: int
    owner_id: int  # Assuming owner_id is an integer
    date_added: str | None = None  # Optional date added in ISO format

    class Config:
        # orm_mode = True
        from_attributes=True