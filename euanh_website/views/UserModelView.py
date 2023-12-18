from typing import Any, Coroutine

from sqladmin import ModelView
from starlette.requests import Request
from wtforms import Form, PasswordField


class UserModelView(ModelView):
    column_exclude_list = ["password"]

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
