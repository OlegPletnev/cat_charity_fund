from sqlalchemy import Column, ForeignKey, Integer, Text

from .base import BaseModal


class Donation(BaseModal):
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))
