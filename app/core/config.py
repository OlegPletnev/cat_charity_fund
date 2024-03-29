from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Благотворительный фонд поддержки котиков QRKot'
    app_description: str = 'Сбор пожертвований в целевые проекты на нужды хвостатых'
    database_url: str = 'sqlite+aiosqlite:///./qpkot.db'
    secret: str = 'SECRET'

    class Config:
        env_file = '.env'


settings = Settings()