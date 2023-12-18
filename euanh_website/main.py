# The basic setup for a FastAPI application
# This file is the entry point for the application

import os

from fastapi import FastAPI
from sqladmin import Admin

from euanh_website.auth import AdminAuth
from euanh_website.views import BlogPostView, UserTokenView, UserView

from . import defaults

app = FastAPI()
admin = Admin(
    app, defaults.engine, authentication_backend=AdminAuth(os.environ["ADMIN_SECRET"])
)
admin.add_view(BlogPostView)
admin.add_view(UserView)
admin.add_view(UserTokenView)


@app.get("/")
async def root():
    return {"message": "Hello World"}
