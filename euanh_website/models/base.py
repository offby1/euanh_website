from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class CommonBase(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_on = Column(DateTime, server_default=func.now(), nullable=False)
    updated_on = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.__dict__}>"

    def __str__(self):
        return f"{self.__class__.__name__} {self.__dict__}"
