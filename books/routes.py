from fastapi import APIRouter

from books.schemas import Book, BookUpdate, BookCreate
from main_app.dependencies import BookServiceDependency

router = APIRouter(
    prefix='/books',
    tags=['books'],
    responses={404: {'detail': 'Not Found'}}
)


@router.get(
    '/',
    name='Получить список кинг',
    response_model=list[Book],
    status_code=200
)
async def get_books(
    offset: int = 0,
    limit: int = 100,
    book_service=BookServiceDependency,
) -> list[Book]:
    return await book_service.get_books(offset, limit=limit)


@router.post(
    '/',
    name='Добавить книгу',
    response_model=Book,
    status_code=201
)
async def create_book(book: BookCreate, book_service=BookServiceDependency) -> Book:
    return await book_service.create_book(book)


@router.get(
    '/{book_id}',
    name='Получить книгу',
    response_model=Book,
    status_code=200
)
async def get_book(book_id: int, book_service=BookServiceDependency) -> Book:
    return await book_service.get_book(book_id)


@router.delete(
    '/{book_id}',
    name='Удалить книгу',
    response_model=Book,
    status_code=200
)
async def delete_book(book_id: int, book_service=BookServiceDependency) -> Book:
    return await book_service.delete_book(book_id)


@router.patch(
    '/{book_id}',
    name='Обновить книгу',
    response_model=Book,
    status_code=200
)
async def update_book(
    book_id: int,
    book: BookUpdate,
    book_service=BookServiceDependency,
) -> Book:
    return await book_service.update_book(book_id, book)
