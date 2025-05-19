import datetime
from typing import Generic, TypeVar

from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from .success_response import SuccessCodes, SuccessResponse

T = TypeVar("T", bound=BaseModel)


class SuccessResult(Generic[T]):
    def __init__(
        self,
        *,
        code: SuccessCodes = SuccessCodes.SUCCESS,
        message: str = "Operation successful",
        status_code: int = 200,
        data: T | None = None,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.data = data

    def to_response_model(self, path: str) -> SuccessResponse[T]:
        return SuccessResponse[T](
            code=self.code,
            message=self.message,
            status=self.status_code,
            data=self.data,
            timestamp=datetime.datetime.now(datetime.timezone.utc),  # RFC 3339-compliant
            path=path,
        )


def success_response_builder(result: SuccessResult[T], request: Request) -> JSONResponse:
    model = result.to_response_model(path=request.url.path)
    return JSONResponse(
        status_code=result.status_code,
        content=model.model_dump(mode="json"),
    )
