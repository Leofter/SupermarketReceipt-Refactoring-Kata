"""Base declarativa do SQLAlchemy para os modelos de banco."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base declarativa compartilhada pelos modelos ORM."""
