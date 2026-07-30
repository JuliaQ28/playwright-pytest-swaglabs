import pytest
from playwright.sync_api import APIRequestContext

from schemas.auth_schema import ErrorResponse, LoginResponse
from schemas.users_schema import CreateUserResponse, UsersListResponse

# 針對 reqres.in 的 API 測試（Case 4）。
# Sauce Demo 本身沒有可測的後端 API，因此改用 reqres.in 作為替代目標，
# 展示「發送 HTTP 請求 -> 用 Pydantic schema 校驗回應結構 -> 斷言業務邏輯」的完整流程。


@pytest.mark.smoke
@pytest.mark.regression
def test_get_users_page_2(api_request_context: APIRequestContext):
    """Case 4.1：GET /api/users?page=2 應回傳 200，且分頁資料非空"""
    response = api_request_context.get("/api/users?page=2")

    assert response.status == 200

    # model_validate 會依 UsersListResponse 定義的欄位與型態檢查回應 JSON，
    # 缺欄位或型態錯誤會直接拋出 ValidationError，比手動檢查 dict key 更精確
    body = UsersListResponse.model_validate(response.json())

    assert body.page == 2
    assert len(body.data) > 0


@pytest.mark.regression
def test_create_user(api_request_context: APIRequestContext):
    """Case 4.2：POST /api/users 建立使用者，應回傳 201 與伺服器產生的 id/createdAt"""
    response = api_request_context.post(
        "/api/users",
        data={"name": "morpheus", "job": "leader"},
    )

    assert response.status == 201

    body = CreateUserResponse.model_validate(response.json())

    assert body.name == "morpheus"
    assert body.job == "leader"
    assert body.id
    assert body.createdAt


@pytest.mark.smoke
@pytest.mark.regression
def test_login_success(api_request_context: APIRequestContext):
    """Case 4.3：POST /api/login 帶入合法帳密，應回傳 200 與非空 token"""
    response = api_request_context.post(
        "/api/login",
        data={"email": "eve.holt@reqres.in", "password": "cityslicka"},
    )

    assert response.status == 200

    body = LoginResponse.model_validate(response.json())

    # 只要 token 不是 None 或空字串，就會通過（真值判斷）
    assert body.token


@pytest.mark.regression
def test_login_missing_password(api_request_context: APIRequestContext):
    """Case 4.4（反向情境）：POST /api/login 只帶 email 不帶 password，應回傳 400 與明確錯誤訊息"""
    response = api_request_context.post(
        "/api/login",
        data={"email": "eve.holt@reqres.in"},
    )

    assert response.status == 400

    body = ErrorResponse.model_validate(response.json())

    assert body.error == "Missing password"
