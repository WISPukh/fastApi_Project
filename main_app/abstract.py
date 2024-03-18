import abc
from typing_extensions import Self

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from main_app.database import get_session


class AbstractService(abc.ABC):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    @classmethod
    def get_service(cls, session: AsyncSession = Depends(get_session)) -> Self:
        return cls(session)
