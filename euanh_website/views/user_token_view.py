from typing import Any, Coroutine

from sqladmin import ModelView
from starlette.requests import Request
from wtforms import Form

from euanh_website.models import UserToken
from euanh_website.services import TokenService


class UserTokenView(ModelView, model=UserToken):
    column_list = [
        UserToken.id,
        UserToken.user,
        UserToken.token,
        UserToken.expires_at,
        UserToken.created_on,
        UserToken.updated_on,
    ]

    form_excluded_columns = ["created_on", "updated_on", UserToken.token]
    column_default_sort = ("created_on", True)

    def on_model_change(
        self, form: Form, model: Any, is_created: bool, request: Request
    ) -> Coroutine[Any, Any, None]:
        if is_created:
            model.token = TokenService().generate_token()
        return super().on_model_change(form, model, is_created, request)
