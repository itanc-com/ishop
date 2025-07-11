from enum import Enum

from fastapi import FastAPI


class AppStates(str, Enum):
    APP_START_TIME = "app_start_time"


def set_app_state(app: FastAPI, key: AppStates, value):
    """Set a state in the FastAPI app."""
    app.state.__setattr__(key.value, value)


def get_app_state(app: FastAPI, key: AppStates):
    """Get a state from the FastAPI app."""
    return app.state.__getattr__(key.value)
