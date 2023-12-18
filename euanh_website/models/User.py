import bcrypt
from sqlalchemy import Column, Integer, String

from euanh_website.models.Base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    email = Column(String, unique=True)
    admin = Column(Integer)

    def __repr__(self):
        return f"<User {self.username}>"

    def __str__(self):
        return self.username

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))
