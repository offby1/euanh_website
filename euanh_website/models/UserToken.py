from datetime import datetime, timedelta, timezone
from typing import Any, Coroutine

from sqladmin import ModelView
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from starlette.requests import Request
from wtforms import Form

from euanh_website.models.Base import CommonBase
from euanh_website.models.User import User
from euanh_website.services import TokenService


class UserToken(CommonBase):
    __tablename__ = "user_tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    token = Column(String(255), nullable=False)
    expires_at = Column(
        DateTime, nullable=False, default=datetime.now(timezone.utc) + timedelta(days=7)
    )

    user = relationship("User", back_populates="tokens")


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
