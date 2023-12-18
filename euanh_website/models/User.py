from typing import Any, Coroutine

import bcrypt
from sqladmin import ModelView
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from starlette.requests import Request
from wtforms import Form, PasswordField

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


class UserView(ModelView, model=User):
    column_list = [
        User.id,
        User.username,
        User.email,
        User.admin,
        User.created_on,
        User.updated_on,
    ]

    form_columns = [User.id, User.username, User.email, User.admin, User.password]

    async def scaffold_form(self) -> Coroutine[Any, Any, type[Form]]:
        form_class = await super().scaffold_form()
        form_class.password = PasswordField("Password")
        return form_class

    def on_model_change(
        self, form: Form, model: Any, is_created: bool, request: Request
    ) -> None:
        if form["password"]:
            model.set_password(form["password"])
            form["password"] = model.password
        else:
            form["password"] = model.password
        return super().on_model_change(form, model, is_created, request)
