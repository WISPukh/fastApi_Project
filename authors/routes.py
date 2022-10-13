from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from books.crud import create_book_for_author as create_book
from books.schemas import Book, BookCreate
from main_app.database import get_db
from . import crud
from .schemas import Author, AuthorUpdate, AuthorCreate

router = APIRouter(
    prefix='/authors',
    tags=['authors'],
    responses={404: {'detail': 'Not Found'}},
)


@router.get("/", response_model=List[Author])
def get_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_authors(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=Author)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)


@router.get("/{author_id}", response_model=Author)
def get_author(author_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_author(db, author_id=author_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete('/{author_id}')
def delete_author(author_id: int, db: Session = Depends(get_db)):
    crud.delete_author(db, author_id)


@router.patch('/{author_id}', response_model=Author)
def update_author(author_id: int, author: AuthorUpdate, db: Session = Depends(get_db)):
    return crud.update_author(db, author_id, author)


@router.post("/{author_id}/book/", response_model=Book)
def create_book_for_author(author_id: int, book: BookCreate, db: Session = Depends(get_db)):
    return create_book(db=db, book=book, author_id=author_id)
