# Приложение QRKot
Учебный проект API приложения для Благотворительного фонда поддержки котиков QRKot. 
Фонд собирает и распределяем пожертвования на различные целевые проекты.

## Технологии

- [FastAPI](https://fastapi.tiangolo.com/)
- [FastAPI Users](https://fastapi-users.github.io/fastapi-users/)
- [SQLAlchemy](http://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [Uvicorn](https://www.uvicorn.org/)

## Запуск
Склонируйте репозиторий  
Создайте и активируйте виртуальное окружение 
```
python -m venv venv
source venv/scripts/activate
```
Активируйте виртуальное окружение  
Установите зависимости 
```
pip install -r requirements.txt
```
Создать файл .env:
```
APP_TITLE=Благотворительный фонд поддержки котиков QRKot
DESCRIPTION=Сбор пожертвований в целевые проекты на нужды хвостатых
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=SECRET
```
Примените миграции для создания файла БД и таблиц
```
alembic upgrade head
```
Запустите сервер из корневой папки проекта
```
uvicorn app.main:app --reload
```

## REST API
Документация API доступна по адресу: http://localhost:8000/docs
