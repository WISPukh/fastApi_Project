from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from books.models import Book as ModelBook
from .models import Author
from .schemas import AuthorCreate, AuthorUpdate


class AuthorService:
    Model = Author

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_author(self, author_id: int) -> Model:
        return await self.get_instance(author_id)

    async def get_authors(
            self, offset: int = 0, limit: int = 100
    ) -> list[Model]:
        return (await self.db.execute(
            select(self.Model).offset(offset).limit(limit)
        )).scalars().all()

    async def create_author(self, data: AuthorCreate) -> Model:
        data.password += '#####fakehash#####'
        author = self.Model(**data.dict())
        self.db.add(author)
        await self.db.commit()

        return author

    async def delete_author(self, author_id: int) -> Model:
        author = await self.get_instance(author_id)
        await self.db.delete(author)
        await self.db.commit()

        return author

    async def update_author(
            self, author_id: int, update_data: AuthorUpdate
    ) -> Model:
        author = await self.get_instance(author_id)
        books = update_data.dict().get('books')
        for key, value in update_data.dict(exclude_unset=True).items():
            if not isinstance(value, list):
                setattr(author, key, value)
            else:
                new_books = (await self.db.execute(
                    select(ModelBook).where(ModelBook.id.in_(books))
                )).scalars().all()
                author.books = new_books
        await self.db.commit()

        return author

    async def get_instance(self, author_id: int) -> Model:
        instance = (await self.db.execute(
            select(self.Model).where(self.Model.id == author_id)
        )).scalars().first()
        if instance is None:
            raise HTTPException(status_code=404, detail='No item found')
        return instance
