from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response

from euanh_website.defaults import Session
from euanh_website.models import User
from euanh_website.services import TokenService


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form.get("username"), form.get("password")

        with Session() as session:
            user = session.query(User).filter_by(username=username).first()
            if user is not None and user.admin and user.check_password(password):
                token = TokenService().create_token(user.id)
                request.session.update({"token": token})
                return True
            else:
                return False

    async def logout(self, request: Request) -> bool:
        token = request.session.get("token")
        TokenService(token).delete_token()
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Response | bool:
        token = request.session.get("token")
        if token is None:
            return RedirectResponse("/admin/login")

        if TokenService(token).verify():
            return True
        else:
            return RedirectResponse("/admin/login")
