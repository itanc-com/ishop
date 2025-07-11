from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.common.exceptions import AppBaseException  # or wherever it lives


async def handle_app_exception(request: Request, exc: AppBaseException):
    error_model = exc.to_response_model(path=request.url.path)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": error_model.model_dump(mode="json")},
    )


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(AppBaseException, handle_app_exception)
