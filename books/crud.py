from fastapi import HTTPException
from sqlalchemy import select

from authors.models import Author as ModelAuthor
from books.models import Book
from books.schemas import BookUpdate, BookCreate
from main_app.abstract import AbstractService


class BookService(AbstractService):
    Model = Book

    async def get_book(self, book_id: int) -> Model:
        return await self.get_instance(book_id)

    async def get_books(
            self, offset: int = 0, limit: int = 100
    ) -> list[Model]:
        return (await self.db.execute(
            select(self.Model).offset(offset).limit(limit)
        )).scalars().all()

    async def delete_book(self, book_id: int) -> Model:
        book = await self.get_instance(book_id)
        await self.db.delete(book)
        await self.db.commit()

        return book

    async def create_book_for_author(
            self, data: BookCreate, author_id: int
    ) -> Model:
        book = self.Model(**data.dict(), author_id=author_id)
        author = (await self.db.execute(
            select(ModelAuthor).where(ModelAuthor.id == author_id)
        )).scalars().first()
        if author is None:
            raise HTTPException(status_code=404, detail='No author exists with given id')
        self.db.add(book)
        await self.db.commit()

        return book

    async def update_book(
            self, book_id: int, data: BookUpdate
    ) -> Model:
        book = await self.get_instance(book_id)
        for key, value in data.dict(exclude_unset=True).items():
            setattr(book, key, value)
        await self.db.commit()

        return book

    async def create_book(self, data: BookCreate) -> Model:
        book = self.Model(**data.dict())
        self.db.add(book)
        await self.db.commit()

        return book

    async def get_instance(self, book_id: int) -> Model:
        instance = (await self.db.execute(
            select(self.Model).where(self.Model.id == book_id)
        )).scalars().first()
        if instance is None:
            raise HTTPException(status_code=404, detail='No item found')
        return instance



