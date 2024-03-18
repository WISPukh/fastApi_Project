import uvicorn
from fastapi import FastAPI
from sqladmin import Admin

import authors.routes
import books.routes
from authors.admin import AuthorAdmin
from main_app.database import engine

# from main_app.middlewares import FakeAccessTokenMiddleware

app = FastAPI()
admin = Admin(app, engine=engine)

admin.add_view(AuthorAdmin)

app.include_router(authors.routes.router)
app.include_router(books.routes.router)


# app.add_middleware(FakeAccessTokenMiddleware)


@app.get('/health')
async def healthcheck():
    return {'health': 'alive'}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
