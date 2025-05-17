from datetime import datetime

from pydantic import BaseModel


class BaseResponse(BaseModel):
    """
    BaseResponse represents the structure of a successful response returned by the API.

    Attributes:
        message (str): A message describing the response.
        status (int): The HTTP status code associated with the response.
        timestamp (datetime): The timestamp when the response was generated.
        path (str): The request path that generated the response.
    """

    status: int
    message: str
    timestamp: datetime
    path: str
