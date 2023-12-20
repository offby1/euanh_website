import os

from fastapi import FastAPI, Request
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from sqladmin import Admin

from euanh_website.admin_views import BlogPostView, UserTokenView, UserView
from euanh_website.auth import AdminAuth
from euanh_website.services import PreviewBlogPostService

from . import defaults
from .defaults import templates

app = FastAPI()
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")),
    name="static",
)
app.add_middleware(GZipMiddleware)

print(templates.env.__dir__())

admin = Admin(
    app,
    defaults.engine,
    authentication_backend=AdminAuth(os.environ["ADMIN_SECRET"]),
    base_url=defaults.site_mapping["admin"],
    templates_dir=templates.env.loader.searchpath,
)
admin.add_view(BlogPostView)
admin.add_view(UserView)
admin.add_view(UserTokenView)


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


@app.get(defaults.site_mapping["blog_posts"])
async def blog(request: Request):
    return templates.TemplateResponse(
        "blog_posts.jinja",
        {
            "request": request,
            "config": defaults.default_jinja_config,
            "site_map": defaults.site_mapping,
            "posts": PreviewBlogPostService.get_all(),
        },
    )


@app.get(defaults.site_mapping["view_blog_post"])
async def view_blog_post(request: Request, id: int):
    post = PreviewBlogPostService.get(id)

    if post is None:
        return templates.TemplateResponse(
            "404.jinja",
            {
                "request": request,
                "config": defaults.default_jinja_config,
                "site_map": defaults.site_mapping,
                "error_message": "Blog post not found",
                "redirect_url": defaults.site_mapping["blog_posts"],
            },
            status_code=404,
        )

    return templates.TemplateResponse(
        "blog.jinja",
        {
            "request": request,
            "config": defaults.default_jinja_config,
            "post": post,
            "site_map": defaults.site_mapping,
        },
    )


@app.exception_handler(404)
async def not_found(request, exc):
    return templates.TemplateResponse(
        "404.jinja",
        {
            "request": request,
            "config": defaults.default_jinja_config,
            "site_map": defaults.site_mapping,
            "error_message": "Page not found",
            "redirect_url": defaults.site_mapping["home"],
        },
        status_code=404,
    )
