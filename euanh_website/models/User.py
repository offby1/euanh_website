import bcrypt
from sqladmin import ModelView
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from wtforms import validators
from wtforms.fields import PasswordField

from euanh_website.models.Base import CommonBase


class User(CommonBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    email = Column(String, unique=True)
    admin = Column(Boolean, default=False)

    blog_posts = relationship("BlogPost", back_populates="author")

    def __repr__(self):
        return f"<User {self.username}>"

    def __str__(self):
        return self.username

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

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

    form_columns = [
        User.id,
        User.username,
        User.email,
        User.admin,
        "password",
    ]

    form_extra_fields = {"password": PasswordField("Password", [validators.Optional()])}

    def on_model_change(self, form, model, is_created):
        # Hash the password if it's provided
        if form.password.data:
            model.set_password(form.password.data)
        return super(UserView, self).on_model_change(form, model, is_created)

    column_formatters = {
        "password": lambda view, context, model, name: "******"  # Mask the password
    }
