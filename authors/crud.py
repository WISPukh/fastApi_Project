from sqlalchemy.orm import Session

from books.models import Book as ModelBook
from . import schemas
from .models import Author as ModelAuthor


def get_author(db: Session, author_id: int):
    return db.query(ModelAuthor).filter(ModelAuthor.id == author_id).first()


def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ModelAuthor).offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.AuthorCreate):
    fake_hashed_password = author.password + '#####fakehash#####'
    db_author = ModelAuthor(email=author.email, password=fake_hashed_password)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def delete_author(db: Session, author_id: int):
    db_author = db.query(ModelAuthor).filter(ModelAuthor.id == author_id).first()
    db.delete(db_author)
    db.commit()


def update_author(db: Session, author_id: int, update_data: schemas.AuthorUpdate):
    db_author = db.query(ModelAuthor).filter(ModelAuthor.id == author_id).first()
    books = update_data.dict().get('books')
    for key, value in update_data.dict(exclude_unset=True).items():
        if not isinstance(value, list):
            setattr(db_author, key, value)
        else:
            all_author_books = db.query(ModelBook).filter(ModelBook.author_id == author_id).all()
            for book in all_author_books:
                book.author_id = None

            needed_books_pks = [book['id'] for book in books]
            books_to_assign = db.query(ModelBook).filter(ModelBook.id.in_(needed_books_pks)).all()
            for book in books_to_assign:
                book.author_id = author_id
    db.commit()
    db.refresh(db_author)
    return db_author
