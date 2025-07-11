from fastapi import FastAPI

from app.core.fastapi.init_app import init_app

app: FastAPI = init_app()
