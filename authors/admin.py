from sqladmin import ModelView

from authors.models import Author

class AuthorAdmin(ModelView, model=Author):
    column_list = [Author.id, Author.email]