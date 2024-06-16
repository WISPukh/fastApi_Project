from typing import Optional

from pydantic import BaseModel, Field

from books.schemas import Book


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
    books: Optional[list[int]]
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
    books: list[Book] = []

    class Config:
        orm_mode = True
