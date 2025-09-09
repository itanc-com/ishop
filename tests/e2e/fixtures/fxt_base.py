from logging import Logger
from typing import Any, Generator

import pytest
from core.logger import get_logger
from playwright.sync_api import APIRequestContext, sync_playwright


@pytest.fixture(autouse=True, scope="session")
def api_request_context() -> Generator[APIRequestContext, Any, None]:
    with sync_playwright() as playwright:
        request_context: APIRequestContext = playwright.request.new_context()
        yield request_context
        request_context.dispose()


@pytest.fixture(autouse=True, scope="session")
def logger() -> Logger:
    return get_logger()
