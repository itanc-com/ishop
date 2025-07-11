from fastapi import FastAPI

from .cors import setup_cors


def setup_middlewares(app: FastAPI):
    setup_cors(app)
