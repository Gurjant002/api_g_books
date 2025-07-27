
from pydantic import BaseModel
from app.schemas.user import NonSensitiveUserSchema


class BookSchemaWithOwner(BaseModel):
    """
    Schema for representing a book with optional ownership information.
    Attributes:
        title (str): The title of the book.
        author (str): The author of the book.
        published_year (int | None): The year the book was published. Optional.
        isbn (str | None): The International Standard Book Number. Optional.
        pages (int | None): The number of pages in the book. Optional.
        cover (str | None): URL or path to the book's cover image. Optional.
        language (str | None): The language in which the book is written. Optional.
        available (bool): Indicates if the book is available. Defaults to True.
        owner_id (int | None): The ID of the user who owns the book. Optional.
        owner (NonSensitiveUserSchema | None): Optional user information for the book's owner.
        date_added (str | None): The date the book was added to the collection. Optional.
    Config:
        from_attributes (bool): Enables attribute-based population of the schema.
    """
    id: int | None = None  # Optional book ID
    title: str
    author: str
    published_year: int | None
    isbn: str | None
    pages: int | None
    cover: str | None
    language: str | None
    available: bool = True  # Default to True for availability
    owner_id: int | None = None  # Optional owner ID for book ownership
    owner: NonSensitiveUserSchema | None  # Optional owner information for book ownership
    date_added: str | None = None  # Optional date added for the book

    class Config:
        # orm_mode = True
        from_attributes=True

class UserBookSchema(BaseModel):
    user: NonSensitiveUserSchema
    readed_books: list[BookSchemaWithOwner]
    rented_books: list[BookSchemaWithOwner]

    class Config:
        # orm_mode = True
        from_attributes=True