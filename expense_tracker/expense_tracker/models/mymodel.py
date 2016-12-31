"""The models for our Expense Tracker."""

from sqlalchemy import (
    Column,
    Integer,
    Float,
    Unicode,
    Date
)

from .meta import Base


class Expense(Base):
    """The expense object."""

    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True)
    item = Column(Unicode)
    amount = Column(Float)
    paid_to = Column(Unicode)
    category = Column(Unicode)
    date = Column(Date)
    description = Column(Unicode)
