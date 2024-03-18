from fastapi import Depends

from authors.crud import AuthorService
from books.crud import BookService

BookServiceDependency: BookService = Depends(BookService.get_service)
AuthorServiceDependency: AuthorService = Depends(AuthorService.get_service)
