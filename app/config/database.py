from http.client import HTTPException
import os
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

@contextmanager
def get_db():
  """
  Context manager for database session handling.

  Yields:
    Session: SQLAlchemy database session object.

  Raises:
    HTTPException: If an exception occurs during database operations, 
    returns a 500 status code with the error detail.

  Ensures:
    - The session is closed after use.
    - Rolls back the session if an exception occurs.
  """
  db = Session()
  try:
    yield db
  except Exception as e:
    db.rollback()
    raise HTTPException(status_code=500, detail=str(e))
  finally:
    db.close()

@contextmanager
def db_transaction():
    """
    Context manager for handling database transactions.

    Yields:
      Session: An active database session.

    Commits the transaction automatically at the end of the block.
    Rolls back the transaction and raises an HTTPException with status code 500 if an error occurs.
    Ensures the database session is closed after the transaction.
    """
    db = Session()
    try:
        yield db
        db.commit()  # ← Commit automático al final
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()