from fastapi import APIRouter

from books.schemas import BookCreate
from main_app.dependencies import BookServiceDependency, AuthorServiceDependency
from authors.schemas import Author, AuthorUpdate, AuthorCreate

router = APIRouter(
    prefix='/authors',
    tags=['authors'],
    responses={404: {'detail': 'Not Found'}},
)


@router.get(
    '/',
    name='Получить список авторов',
    response_model=list[Author],
    status_code=200
)
async def get_authors(
    offset: int = 0,
    limit: int = 100,
    author_service=AuthorServiceDependency,
) -> list[Author]:
    return await author_service.get_authors(offset, limit)


@router.post(
    '/',
    name='Добавить автора',
    response_model=Author,
    status_code=201
)
async def create_author(author: AuthorCreate, author_service=AuthorServiceDependency) -> Author:
    return await author_service.create_author(author)


@router.get(
    '/{author_id}',
    name='Получить автора',
    response_model=Author,
    status_code=200
)
async def get_author(author_id: int, author_service=AuthorServiceDependency) -> Author:
    return await author_service.get_author(author_id)


@router.delete(
    '/{author_id}',
    name='Удалить автора',
    response_model=Author,
    status_code=200
)
async def delete_author(author_id: int, author_service=AuthorServiceDependency) -> Author:
    return await author_service.delete_author(author_id)


@router.patch(
    '/{author_id}',
    name='Обновить автора',
    response_model=Author,
    status_code=200
)
async def update_author(
    author_id: int,
    author: AuthorUpdate,
    author_service=AuthorServiceDependency,
) -> Author:
    return await author_service.update_author(author_id, author)


@router.post(
    '/{author_id}/book/',
    name='Добавить автору книгу',
    description='Добавляет новую книгу в базу данных и сразу назначает ее конкретному автору',
    response_model=Author,
    status_code=200
)
async def create_book_for_author(
    author_id: int,
    book: BookCreate,
    book_service=BookServiceDependency
) -> Author:
    return await book_service.create_book_for_author(book, author_id)
