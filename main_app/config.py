from dotenv import load_dotenv
from pydantic import BaseSettings, PostgresDsn, validator

load_dotenv()


class Settings(BaseSettings):
    ACCESS_TOKEN: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    DATABASE_URL: str = ''

    @validator('DATABASE_URL', pre=True)
    def get_postgresql_dsn(cls, v, values) -> str:
        if v:
            return v
        return PostgresDsn.build(
            scheme='postgresql+asyncpg',
            user=values.get('POSTGRES_USER'),
            password=values.get('POSTGRES_PASSWORD'),
            host=values.get('POSTGRES_HOST'),
            port=str(values.get('POSTGRES_PORT')),
            # path=values.get('POSTGRES_DB'),
        )

    class Config:
        env_file = '../.env'
        env_file_encoding = 'utf-8'


settings = Settings()
