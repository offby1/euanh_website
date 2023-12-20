from typing import Any, Coroutine

from sqladmin import ModelView
from starlette.requests import Request
from wtforms import Form, PasswordField

from euanh_website.models import User


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
    ) -> Coroutine[Any, Any, None]:
        if form["password"]:
            model.set_password(form["password"])
            form["password"] = model.password
        else:
            form["password"] = model.password
        return super().on_model_change(form, model, is_created, request)
