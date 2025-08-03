from app.config.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

class Book(Base):
    """
    Modelo de datos para libros en la base de datos.
    
    Esta clase representa la tabla 'books' que almacena información básica
    de los libros disponibles en el sistema.
    
    Attributes:
        id (int): Identificador único del libro (clave primaria)
        title (str): Título del libro (máximo 255 caracteres, obligatorio)
        author (str): Nombre del autor del libro (obligatorio)
        published_year (int): Año de publicación del libro (opcional)
        isbn (str): Código ISBN del libro (opcional)
        pages (int): Número de páginas del libro (opcional)
        cover (str): URL o ruta de la imagen de portada del libro (opcional)
        language (str): Idioma del libro (opcional)
        description (str): Descripción o sinopsis del libro (opcional)
        available (bool): Indica si el libro está disponible (por defecto True)
    
    Note:
        Los campos title e isbn pueden configurarse como únicos activando
        las opciones unique=True en sus respectivas definiciones.
    """
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(length=255), unique=False, nullable=False) # Activate unique=True for title
    author = Column(String, nullable=False)
    published_year = Column(Integer, nullable=True)
    isbn = Column(String, unique=False, nullable=True) # Activate unique=True for isbn
    pages = Column(Integer, nullable=True)
    cover = Column(String, nullable=True)
    language = Column(String, nullable=True)
    description = Column(String, nullable=True)
    available = Column(Boolean, default=True)  # Default to 1 for availability
    date_added = Column(String, nullable=True)  # Assuming date_added is a string in ISO format

    owners = relationship("BookOwner", back_populates="book")

class BookOwner(Base):
    """
    Modelo de datos para la relación de propiedad entre usuarios y libros.
    
    Esta clase representa la tabla 'book_owners' que establece qué usuarios
    poseen qué libros en el sistema, creando una relación muchos a muchos
    entre usuarios y libros.
    
    Attributes:
        id (int): Identificador único de la relación (clave primaria)
        book_id (int): ID del libro (referencia a la tabla books)
        owner_id (int): ID del usuario propietario (referencia a la tabla users)
        date_added (str): Fecha en que se agregó el libro a la colección del usuario
                         (formato ISO string, opcional)
    
    Note:
        Esta tabla actúa como tabla intermedia para relacionar usuarios con
        sus libros, permitiendo que un usuario tenga múltiples libros y que
        un libro pueda tener múltiples propietarios.
    """
    __tablename__ = 'book_owners'

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Assuming owner_id is an integer
    date_added = Column(String, nullable=True)  # Assuming date_added is a string in ISO format

    book = relationship("Book", back_populates="owners")
    user = relationship("User", back_populates="owned_books")

class ReadedBook(Base):
    """
    Modelo de datos para el seguimiento de libros leídos por los usuarios.
    
    Esta clase representa la tabla 'readed_books' que registra qué libros
    han sido leídos por qué usuarios, incluyendo las fechas de inicio y
    finalización de la lectura.
    
    Attributes:
        id (int): Identificador único del registro de lectura (clave primaria)
        book_id (int): ID del libro leído (referencia a la tabla books)
        user_id (int): ID del usuario que leyó el libro (referencia a la tabla users)
        start (str): Fecha de inicio de la lectura (formato ISO string, opcional)
        end (str): Fecha de finalización de la lectura (formato ISO string, opcional)
    
    Note:
        Esta tabla permite llevar un historial de lectura de cada usuario,
        útil para generar estadísticas, recomendaciones y seguimiento del
        progreso de lectura.
    """
    __tablename__ = 'readed_books'

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Assuming user_id is an integer
    start = Column(String, nullable=True)  # Assuming start is a string in ISO format
    end = Column(String, nullable=True)  # Assuming end is a string in ISO format

class BookedBook(Base):
    """
    Modelo de datos para el seguimiento de libros que un usuario ha marcado como leídos.
    
    Esta clase representa la tabla 'booked_books' que registra qué libros
    han sido marcados como leídos por los usuarios, junto con las fechas
    de inicio y finalización de la lectura.
    
    Attributes:
        id (int): Identificador único del registro de libro leído (clave primaria)
        book_id (int): ID del libro leído (referencia a la tabla books)
        user_id (int): ID del usuario que leyó el libro (referencia a la tabla users)
        start (str): Fecha de inicio de la lectura (formato ISO string, opcional)
        end (str): Fecha de finalización de la lectura (formato ISO string, opcional)
    
    Note:
        Esta tabla permite llevar un registro detallado de los libros leídos
        por cada usuario, facilitando el seguimiento del progreso y las
        estadísticas de lectura.
    """
    __tablename__ = 'booked_books'

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Assuming user_id is an integer
    start = Column(String, nullable=True)  # Assuming start is a string in ISO format
    end = Column(String, nullable=True)  # Assuming end is a string in ISO format