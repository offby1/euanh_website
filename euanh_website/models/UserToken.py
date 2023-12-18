from datetime import datetime, timedelta, timezone

from sqladmin import ModelView
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from euanh_website.models.Base import CommonBase
from euanh_website.models.User import User


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

    form_excluded_columns = ["created_on", "updated_on"]
    column_default_sort = ("created_on", True)
