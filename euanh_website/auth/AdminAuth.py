from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from euanh_website.defaults import Session
from euanh_website.models import User


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form.get("username"), form.get("password")

        with Session() as session:
            user = session.query(User).filter_by(username=username).first()
            if user is not None and user.admin and user.check_password(password):
                return True
            else:
                return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True
