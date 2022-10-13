from typing import Optional, List

from pydantic import BaseModel, Field

from books.schemas import Book, BookChangeAuthor


class AuthorBase(BaseModel):
    email: str = Field(regex=r'\S+\w+@\w+\S+')

    class Config:
        fields = {
            'email': {
                'example': 'sas@sos.ru'
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
                'title': 'sas',
                'example': None
            },
            'email': {
                'title': 'emaaaaaail',
                'example': 'sas@jij.ru'
            },
        }


class Author(AuthorBase):
    id: int
    is_active: bool = True
    books: List[Book] = []

    class Config:
        orm_mode = True
