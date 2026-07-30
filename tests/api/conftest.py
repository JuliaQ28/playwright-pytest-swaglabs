import os

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Playwright, APIRequestContext

# 從專案根目錄的 .env 讀取環境變數（本機開發用；CI 環境則改由 GitHub Actions Secrets 注入，
# 兩者都是透過同一個 REQRES_API_KEY 環境變數名稱讀取，程式碼本身不需要區分來源）。
load_dotenv()

BASE_URL = "https://reqres.in"


@pytest.fixture(scope="session")
def api_request_context(playwright: Playwright) -> APIRequestContext:
    """建立一個帶有 API Key 的 APIRequestContext，整個測試 session 只建立一次 (scope="session")，
    所有 API 測試共用同一組已設定好 base_url 與 headers 的連線設定。
    """
    api_key = os.environ.get("REQRES_API_KEY")
    if not api_key:
        # 沒有金鑰時直接跳過而非讓測試失敗，方便沒有設定 .env 的人也能跑其餘測試
        pytest.skip("REQRES_API_KEY 環境變數未設定，跳過 API 測試")

    request_context = playwright.request.new_context(
        base_url=BASE_URL,
        extra_http_headers={
            "x-api-key": api_key,
            "Content-Type": "application/json",
        },
    )
    yield request_context
    # yield 之後的程式碼在 session 結束時執行，確保連線資源被釋放
    request_context.dispose()
