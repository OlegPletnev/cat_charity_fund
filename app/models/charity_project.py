from sqlalchemy import Column, String, Text

from .base import BaseModal


class CharityProject(BaseModal):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return self.name[:10]
