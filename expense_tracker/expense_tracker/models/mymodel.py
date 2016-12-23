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

    def to_json(self):
        jsonify = {
            "id": self.id,
            "item": self.item,
            "amount": self.amount,
            "paid_to": self.paid_to,
            "category": self.category,
            "date": self.date.strftime("%b %d, %Y"),
            "description": self.description,
        }
        return jsonify

