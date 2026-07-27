import os

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Playwright, APIRequestContext

load_dotenv()

BASE_URL = "https://reqres.in"


@pytest.fixture(scope="session")
def api_request_context(playwright: Playwright) -> APIRequestContext:
    api_key = os.environ.get("REQRES_API_KEY")
    if not api_key:
        pytest.skip("REQRES_API_KEY 環境變數未設定，跳過 API 測試")

    request_context = playwright.request.new_context(
        base_url=BASE_URL,
        extra_http_headers={
            "x-api-key": api_key,
            "Content-Type": "application/json",
        },
    )
    yield request_context
    request_context.dispose()
