import uvicorn
from fastapi import FastAPI

import authors.routes
import books.routes
import middlewares

app = FastAPI()

app.include_router(authors.routes.router)
app.include_router(books.routes.router)

app.add_middleware(middlewares.FakeAccessTokenMiddleware)


@app.get("/health")
async def healthcheck():
    return {"health": "alive"}


if __name__ == '__main__':
    uvicorn.run('main:app', debug=True, reload=True)
