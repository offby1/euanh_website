from datetime import datetime

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CommonBase(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_on = Column(DateTime)
    updated_on = Column(DateTime)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.__dict__}>"

    def __str__(self):
        return f"{self.__class__.__name__} {self.__dict__}"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.created_on = datetime.now()
        self.updated_on = datetime.now()

    def update(self):
        self.updated_on = datetime.now()
