from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from books import schemas
from books.crud import BookService
from main_app.database import get_db

router = APIRouter(
    prefix='/books',
    tags=['books'],
    responses={404: {'detail': 'Not Found'}}
)


@router.get('/', response_model=List[schemas.Book])
async def get_books(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_service(db).get_books(offset, limit=limit)


@router.post('/', response_model=schemas.Book)
async def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return get_service(db).create_book(book)


@router.get('/{book_id}', response_model=schemas.Book)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    return get_service(db).get_book(book_id)


@router.delete('/{book_id}')
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    get_service(db).delete_book(book_id)


@router.patch('/{book_id}', response_model=schemas.Book)
async def update_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)):
    return get_service(db).update_book(book_id, book)


def get_service(db: Session):
    return BookService(db)
