from pydantic import BaseModel

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
        owner_id (int | None): The ID of the owner of the book. Optional.
        date_added (str | None): The date the book was added to the collection. Optional.
    Config:
        from_attributes (bool): Enables attribute-based population of the schema.
    """
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

class BookSchema(BaseModel):
    """
    Schema representing a book entity.
    Attributes:
        title (str): The title of the book.
        author (str): The author of the book.
        published_year (int | None): The year the book was published. Optional.
        isbn (str | None): The International Standard Book Number. Optional.
        pages (int | None): The number of pages in the book. Optional.
        cover (str | None): The URL or path to the book's cover image. Optional.
        language (str | None): The language the book is written in. Optional.
        available (bool): Indicates if the book is available. Defaults to True.
        date_added (str | None): The date the book was added to the system. Optional.
    """
    title: str
    author: str
    published_year: int | None
    isbn: str | None
    pages: int | None
    cover: str | None
    language: str | None
    available: bool = True  # Default to True for availability
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

class OwnerBookSchema(BaseModel):
    """
    Schema representing the relationship between a book and its owner.
    Attributes:
        book_id (int): Unique identifier of the book.
        owner_id (int): Unique identifier of the owner.
        date_added (str | None): Optional date when the book was added, in ISO format.
    Config:
        from_attributes (bool): Enables loading data from ORM objects.
    """
    book_id: int
    owner_id: int  # Assuming owner_id is an integer
    date_added: str | None = None  # Optional date added in ISO format

    class Config:
        # orm_mode = True
        from_attributes=True