
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
    date_added: str | None = None  # Optional date: the date the book was added

    class Config:
        # orm_mode = True
        from_attributes=True

class BorrowSchema(BaseModel):
    """
    Schema for representing a book borrowing record.
    Attributes:
        id (int): The unique identifier for the borrowing record.
        book_id (int): The ID of the book being borrowed.
        user_id (int): The ID of the user borrowing the book.
        start (str): The start date of the borrowing period in ISO format.
        end (str): The end date of the borrowing period in ISO format.
    """
    id: int
    book_id: int
    user_id: int
    start: str  # Start date in ISO format
    end: str  # End date in ISO format