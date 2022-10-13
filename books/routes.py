from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from books import crud
from books import schemas
from main_app.database import get_db

router = APIRouter(
    prefix='/books',
    tags=['books'],
    responses={404: {'detail': 'Not Found'}}
)


@router.get("/", response_model=List[schemas.Book])
def get_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_books(db, skip=skip, limit=limit)


@router.post('/', response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, book)


@router.get('/{book_id}', response_model=schemas.Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    return crud.get_book(db, book_id)


@router.delete('/{book_id}')
def delete_book(book_id: int, db: Session = Depends(get_db)):
    crud.delete_book(db, book_id)


@router.patch('/{book_id}', response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)):
    return crud.update_book(db, book_id, book)
