from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from books.crud import BookService
from books.schemas import BookCreate
from main_app.database import get_session
from .crud import AuthorService
from .schemas import Author, AuthorUpdate, AuthorCreate

router = APIRouter(
    prefix='/authors',
    tags=['authors'],
    responses={404: {'detail': 'Not Found'}},
)


@router.get('/',
            name='Получить список авторов',
            response_model=list[Author],
            status_code=200)
async def get_authors(offset: int = 0,
                      limit: int = 100,
                      db: AsyncSession = Depends(get_session)) -> list[Author]:
    return await AuthorService(db).get_authors(offset, limit)


@router.post('/',
             name='Добавить автора',
             response_model=Author,
             status_code=201)
async def create_author(author: AuthorCreate,
                        session: AsyncSession = Depends(get_session)) -> Author:
    return await AuthorService(session).create_author(author)


@router.get('/{author_id}',
            name='Получить автора',
            response_model=Author,
            status_code=200)
async def get_author(author_id: int,
                     session: AsyncSession = Depends(get_session)) -> Author:
    return await AuthorService(session).get_author(author_id)


@router.delete('/{author_id}',
               name='Удалить автора',
               response_model=Author,
               status_code=200)
async def delete_author(author_id: int,
                        session: AsyncSession = Depends(get_session)) -> Author:
    return await AuthorService(session).delete_author(author_id)


@router.patch('/{author_id}',
              name='Обновить автора',
              response_model=Author,
              status_code=200)
async def update_author(author_id: int,
                        author: AuthorUpdate,
                        session: AsyncSession = Depends(get_session)) -> Author:
    return await AuthorService(session).update_author(author_id, author)


@router.post('/{author_id}/book/',
             name='Добавить автору книгу',
             description='Добавляет новую книгу в базу данных и '
                         'сразу назначает ее конкретному автору',
             response_model=Author,
             status_code=200)
async def create_book_for_author(author_id: int,
                                 book: BookCreate,
                                 session: AsyncSession = Depends(get_session)) -> Author:
    return await BookService(session).create_book_for_author(book, author_id)
