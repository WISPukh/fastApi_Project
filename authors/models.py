from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from main_app.database import Base


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    books = relationship('Book', back_populates='author', lazy='subquery')
