from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):

    async def get_for_user(
            self,
            user: User,
            session: AsyncSession,
    ) -> List[Donation]:
        donations = await session.scalars(select(self.model).where(
            self.model.user_id == user.id
        ))
        return donations.all()


donation_crud = CRUDDonation(Donation)
