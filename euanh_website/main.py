import os

from fastapi import FastAPI, Request
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqladmin import Admin

from euanh_website.auth import AdminAuth
from euanh_website.views import BlogPostView, UserTokenView, UserView

from . import defaults

app = FastAPI()
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")),
    name="static",
)
app.add_middleware(GZipMiddleware)

admin = Admin(
    app, defaults.engine, authentication_backend=AdminAuth(os.environ["ADMIN_SECRET"])
)
admin.add_view(BlogPostView)
admin.add_view(UserView)
admin.add_view(UserTokenView)

templates = Jinja2Templates(
    directory=os.path.join(os.path.dirname(__file__), "templates")
)


@app.get("/")
async def root(request: Request):
    # Get the index template from the templates folder using jinja2
    return templates.TemplateResponse(
        "index.jinja", {"request": request, "config": defaults.default_jinja_config}
    )
