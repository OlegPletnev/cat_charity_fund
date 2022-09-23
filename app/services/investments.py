from datetime import datetime
from typing import Union, List, Type

from sqlalchemy import select, false
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import ModelType
from app.models import CharityProject, Donation


async def get_open_objects(
        model: Type[ModelType],
        session: AsyncSession
) -> List[Union[CharityProject, Donation]]:
    """Получить все открытые проекты или пожертвования."""
    open_objects = await session.execute(
        select(model)
        .where(
            model.fully_invested == false()
        ).order_by(
            model.create_date
        ))
    return open_objects.scalars().all()


async def investment(
    new_obj: Union[CharityProject, Donation],
    session: AsyncSession,
) -> None:
    """
    Запуск процесса 'инвестирования' сразу после создания
    нового проекта или нового пожертвования.
    """
    model = CharityProject if isinstance(new_obj, Donation) else Donation
    open_objects = await get_open_objects(model, session)
    rest_donat = new_obj.full_amount
    for obj in open_objects:
        donat = min(rest_donat, obj.full_amount - obj.invested_amount)
        obj.invested_amount += donat
        new_obj.invested_amount += donat
        rest_donat -= donat

        if obj.full_amount == obj.invested_amount:
            obj.fully_invested = True
            obj.close_date = datetime.now()
        if rest_donat == 0:
            new_obj.fully_invested = True
            new_obj.close_date = datetime.now()
            break
    await session.commit()
