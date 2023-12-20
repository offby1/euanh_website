import os

from fastapi import FastAPI, Request
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqladmin import Admin

from euanh_website.auth import AdminAuth
from euanh_website.services import PreviewBlogPostService
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
    app,
    defaults.engine,
    authentication_backend=AdminAuth(os.environ["ADMIN_SECRET"]),
    base_url=defaults.site_mapping["admin"],
)
admin.add_view(BlogPostView)
admin.add_view(UserView)
admin.add_view(UserTokenView)

templates = Jinja2Templates(
    directory=os.path.join(os.path.dirname(__file__), "templates")
)


@app.get(defaults.site_mapping["home"])
async def root(request: Request):
    # Get the index template from the templates folder using jinja2
    return templates.TemplateResponse(
        "index.jinja",
        {
            "request": request,
            "config": defaults.default_jinja_config,
            "posts": PreviewBlogPostService.get_latest(limit=6),
            "site_map": defaults.site_mapping,
        },
    )


@app.get(defaults.site_mapping["about"])
async def about(request: Request):
    return templates.TemplateResponse(
        "about.jinja",
        {
            "request": request,
            "config": defaults.default_jinja_config,
            "site_map": defaults.site_mapping,
        },
    )


@app.get(defaults.site_mapping["contact"])
async def contact(request: Request):
    return templates.TemplateResponse(
        "contact.jinja",
        {
            "request": request,
            "config": defaults.default_jinja_config,
            "site_map": defaults.site_mapping,
        },
    )
