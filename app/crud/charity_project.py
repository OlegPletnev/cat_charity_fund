from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas.charity_project import (CharityProjectUpdate,
                                         CharityProjectCreate)


class CRUDCharityProject(CRUDBase[
    CharityProject,
    CharityProjectCreate,
    CharityProjectUpdate
]):

    async def get_project_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> Optional[CharityProject]:
        db_project_id = await session.execute(
            select(CharityProject).where(
                CharityProject.name == project_name
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    async def update(
        self,
        db_obj: CharityProject,
        project_in: CharityProjectUpdate,
        session: AsyncSession,
    ) -> CharityProject:
        obj_data = jsonable_encoder(db_obj)
        update_data = project_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj: CharityProject,
        session: AsyncSession,
    ) -> CharityProject:
        await session.delete(db_obj)
        await session.commit()
        return db_obj


charity_project_crud = CRUDCharityProject(CharityProject)
