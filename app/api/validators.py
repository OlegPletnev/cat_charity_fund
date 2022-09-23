from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    """Проверяем уникальность проекта по названию."""
    project = await charity_project_crud.get_by_attribute(
        'name', project_name, session
    )
    if project:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """Проверяем, что проект существует."""
    project = await charity_project_crud.get_by_attribute(
        'id', project_id, session
    )
    if not project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return project


async def check_project_before_update(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession,
) -> CharityProject:
    """
    Проверить, что проект можно обновить, он не закрыт
    и требуемую сумму не делают меньше уже внесенных инвестиций.
    """
    project = await charity_project_crud.get_by_attribute(
        'id', project_id, session
    )
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!',
        )
    if obj_in.full_amount and project.invested_amount > obj_in.full_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Нельзя установить требуемую сумму меньше уже вложенной!',
        )

    return project


async def check_project_before_delete(
        project_id: int,
        session: AsyncSession
) -> CharityProject:
    """Проверяем перед удалением, что в проекте нет инвестиций."""
    project = await charity_project_crud.get_by_attribute(
        'id', project_id, session
    )
    if project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!',
        )
    return project
