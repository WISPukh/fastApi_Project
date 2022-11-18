from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from main_app.database import get_session
from .crud import BookService
from .schemas import Book, BookUpdate, BookCreate

router = APIRouter(
    prefix='/books',
    tags=['books'],
    responses={404: {'detail': 'Not Found'}}
)


@router.get('/',
            name='Получить список кинг',
            response_model=list[Book],
            status_code=200)
async def get_books(offset: int = 0,
                    limit: int = 100,
                    session: AsyncSession = Depends(get_session)) -> list[Book]:
    return await BookService(session).get_books(offset, limit=limit)


@router.post('/',
             name='Добавить книгу',
             response_model=Book,
             status_code=201)
async def create_book(book: BookCreate,
                      session: AsyncSession = Depends(get_session)) -> Book:
    return await BookService(session).create_book(book)


@router.get('/{book_id}',
            name='Получить книгу',
            response_model=Book,
            status_code=200)
async def get_book(book_id: int,
                   session: AsyncSession = Depends(get_session)) -> Book:
    return await BookService(session).get_book(book_id)


@router.delete('/{book_id}',
               name='Удалить книгу',
               response_model=Book,
               status_code=200)
async def delete_book(book_id: int,
                      session: AsyncSession = Depends(get_session)) -> Book:
    return await BookService(session).delete_book(book_id)


@router.patch('/{book_id}',
              name='Обновить книгу',
              response_model=Book,
              status_code=200)
async def update_book(book_id: int,
                      book: BookUpdate,
                      session: AsyncSession = Depends(get_session)) -> Book:
    return await BookService(session).update_book(book_id, book)
