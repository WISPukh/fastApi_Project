from sqlalchemy.orm import Session

from books.models import Book as ModelBook
from . import schemas
from .models import Author as ModelAuthor


class AuthorService:
    def __init__(self, db: Session):
        self.db = db

    def get_author(self, author_id: int):
        return self.db.query(ModelAuthor).filter(ModelAuthor.id == author_id).first()

    def get_authors(self, offset: int = 0, limit: int = 100):
        return self.db.query(ModelAuthor).offset(offset).limit(limit).all()

    def create_author(self, author: schemas.AuthorCreate):
        fake_hashed_password = author.password + '#####fakehash#####'
        db_author = ModelAuthor(email=author.email, password=fake_hashed_password)
        self.db.add(db_author)
        self.db.commit()
        self.db.refresh(db_author)
        return db_author

    def delete_author(self, author_id: int):
        db_author = self.db.query(ModelAuthor).filter(ModelAuthor.id == author_id).first()
        self.db.delete(db_author)
        self.db.commit()

    def update_author(self, author_id: int, update_data: schemas.AuthorUpdate):
        db_author = self.db.query(ModelAuthor).filter(ModelAuthor.id == author_id).first()
        books = update_data.dict().get('books')
        for key, value in update_data.dict(exclude_unset=True).items():
            if not isinstance(value, list):
                setattr(db_author, key, value)
            else:
                all_author_books = self.db.query(ModelBook).filter(ModelBook.author_id == author_id).all()
                for book in all_author_books:
                    book.author_id = None

                needed_books_pks = [book['id'] for book in books]
                books_to_assign = self.db.query(ModelBook).filter(ModelBook.id.in_(needed_books_pks)).all()
                for book in books_to_assign:
                    book.author_id = author_id
        self.db.commit()
        self.db.refresh(db_author)
        return db_author
