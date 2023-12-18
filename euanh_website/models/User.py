import bcrypt
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from euanh_website.models.Base import CommonBase


class User(CommonBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    email = Column(String, unique=True)
    admin = Column(Boolean, default=False)

    blog_posts = relationship("BlogPost", back_populates="author")
    tokens = relationship("UserToken", back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"

    def __str__(self):
        return self.username

    def set_password(self, password):
        self.password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode()

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))
