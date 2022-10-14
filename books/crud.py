from sqlalchemy.orm import Session

from .models import Book as ModelBook
from .schemas import BookUpdate, BookCreate


class BookService:
    def __init__(self, db: Session):
        self.db = db

    def get_books(self, offset: int = 0, limit: int = 100):
        return self.db.query(ModelBook).offset(offset).limit(limit).all()

    def get_book(self, book_id: int):
        return self.db.query(ModelBook).filter(ModelBook.id == book_id).first()

    def create_book_for_author(self, book: BookCreate, author_id: int):
        db_book = ModelBook(**book.dict(), author_id=author_id)
        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)
        return db_book

    def delete_book(self, book_id: int):
        db_book = self.db.query(ModelBook).filter(ModelBook.id == book_id).first()
        self.db.delete(db_book)
        self.db.commit()

    def update_book(self, book_id: int, book: BookUpdate):
        db_book = self.db.query(ModelBook).filter(ModelBook.id == book_id).first()
        for key, value in book.dict(exclude_unset=True).items():
            setattr(db_book, key, value)
        self.db.commit()
        return db_book

    def create_book(self, book: BookCreate):
        db_book = ModelBook(**book.dict())
        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)
        return db_book
