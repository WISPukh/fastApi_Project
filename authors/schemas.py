from typing import Optional, List

from pydantic import BaseModel, Field

from books.schemas import Book, BookChangeAuthor


class AuthorBase(BaseModel):
    email: str = Field(regex=r'\S+\w+@\w+\S+')

    class Config:
        fields = {
            'email': {
                'example': 'e.mail@what.com'
            }
        }


class AuthorCreate(AuthorBase):
    password: str


class AuthorUpdate(BaseModel):
    books: Optional[List[BookChangeAuthor]]
    email: Optional[str] = Field(regex=r'\S+\w+@\w+\S+')

    class Config:
        fields = {
            'books': {
                'title': 'books',
                'example': None
            },
            'email': {
                'title': 'email',
                'example': 'e.mail@what.com'
            },
        }


class Author(AuthorBase):
    id: int
    is_active: bool = True
    books: List[Book] = []

    class Config:
        orm_mode = True
