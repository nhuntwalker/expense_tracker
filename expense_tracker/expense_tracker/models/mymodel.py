from sqlalchemy import (
    Column,
    Index,
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




# class MyModel(Base):
#     __tablename__ = 'models'
#     id = Column(Integer, primary_key=True)
#     name = Column(Text)
#     value = Column(Integer)


# Index('my_index', MyModel.name, unique=True, mysql_length=255)
