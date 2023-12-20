import os

import requests
from fastapi import FastAPI, Form, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
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
async def home(request: Request):
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
            "url": defaults.site_mapping["contact"],
        },
    )


@app.post(defaults.site_mapping["contact"])
async def contact_form_submission(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
    recaptcha_response: str = Form(...),
):
    # Verify the reCAPTCHA response
    data = {"secret": defaults.recaptcha_secret_key, "response": recaptcha_response}
    response = requests.post(
        "https://www.google.com/recaptcha/api/siteverify", data=data
    )
    result = response.json()

    # Check if reCAPTCHA test passed
    if not result.get("success") or result.get("score") < defaults.is_a_bot_threshold:
        return templates.TemplateResponse(
            "contact_success.jinja",
            {
                "request": request,
                "config": defaults.default_jinja_config,
                "site_map": defaults.site_mapping,
            },
        )

    # Return a success message
    return templates.TemplateResponse(
        "contact_success.jinja",
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


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"detail": exc.errors()})
