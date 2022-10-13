from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from books.crud import BookService
from books.schemas import Book, BookCreate
from main_app.database import get_db
from .crud import AuthorService
from .schemas import Author, AuthorUpdate, AuthorCreate

router = APIRouter(
    prefix='/authors',
    tags=['authors'],
    responses={404: {'detail': 'Not Found'}},
)


@router.get('/', response_model=List[Author])
async def get_authors(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_service(db).get_authors(offset, limit)


@router.post('/', response_model=Author)
async def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    return get_service(db).create_author(author)


@router.get('/{author_id}', response_model=Author)
async def get_author(author_id: int, db: Session = Depends(get_db)):
    db_user = get_service(db).get_author(author_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user


@router.delete('/{author_id}')
async def delete_author(author_id: int, db: Session = Depends(get_db)):
    get_service(db).delete_author(author_id)


@router.patch('/{author_id}', response_model=Author)
async def update_author(author_id: int, author: AuthorUpdate, db: Session = Depends(get_db)):
    return get_service(db).update_author(author_id, author)


@router.post('/{author_id}/book/', response_model=Book)
async def create_book_for_author(author_id: int, book: BookCreate, db: Session = Depends(get_db)):
    return BookService(db).create_book_for_author(book, author_id)


def get_service(db: Session):
    return AuthorService(db)
