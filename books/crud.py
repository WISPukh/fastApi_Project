from sqlalchemy.orm import Session

from .models import Book as ModelBook
from .schemas import BookUpdate, BookCreate


def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ModelBook).offset(skip).limit(limit).all()


def get_book(db: Session, book_id: int):
    return db.query(ModelBook).filter(ModelBook.id == book_id).first()


def create_book_for_author(db: Session, book: BookCreate, author_id: int):
    db_book = ModelBook(**book.dict(), author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int):
    db_book = db.query(ModelBook).filter(ModelBook.id == book_id).first()
    db.delete(db_book)
    db.commit()


def update_book(db: Session, book_id: int, book: BookUpdate):
    db_book = db.query(ModelBook).filter(ModelBook.id == book_id).first()
    for key, value in book.dict(exclude_unset=True).items():
        setattr(db_book, key, value)
    db.commit()
    return db_book


def create_book(db: Session, book: BookCreate):
    db_book = ModelBook(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
