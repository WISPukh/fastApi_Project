from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class BookBase(BaseModel):
    title: str = Field(min_length=5)
    price: PositiveInt = 1
    description: Optional[str] = Field(min_length=5)


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    author_id: Optional[int]

    class Config:
        orm_mode = True


class BookUpdate(BookBase):
    title: Optional[str]
    price: Optional[PositiveInt]
    description: Optional[str]


class ListBook(BaseModel):
    items: list[Book]
