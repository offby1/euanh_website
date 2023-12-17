# The basic setup for a FastAPI application
# This file is the entry point for the application

from fastapi import FastAPI
from sqladmin import Admin, ModelView

from . import config

app = FastAPI()
admin = Admin(app, config.engine)


@app.get("/")
async def root():
    return {"message": "Hello World"}
