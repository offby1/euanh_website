# The basic setup for a FastAPI application
# This file is the entry point for the application

from fastapi import FastAPI
from sqladmin import Admin, ModelView

from euanh_website.models import (BlogPost, BlogPostView, User, UserTokenView,
                                  UserView)

from . import defaults

app = FastAPI()
admin = Admin(app, defaults.engine)
admin.add_view(BlogPostView)
admin.add_view(UserView)
admin.add_view(UserTokenView)


@app.get("/")
async def root():
    return {"message": "Hello World"}
