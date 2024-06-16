from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from main_app.database import Base


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String)
    price = Column(Integer)
    description = Column(String, index=True)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=True)

    author = relationship('Author', back_populates='books')
