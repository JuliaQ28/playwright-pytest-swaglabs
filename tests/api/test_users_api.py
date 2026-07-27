from playwright.sync_api import APIRequestContext

from schemas.auth_schema import LoginResponse
from schemas.users_schema import CreateUserResponse, UsersListResponse


def test_get_users_page_2(api_request_context: APIRequestContext):
    response = api_request_context.get("/api/users?page=2")

    assert response.status == 200

    body = UsersListResponse.model_validate(response.json())

    assert body.page == 2
    assert len(body.data) > 0


def test_create_user(api_request_context: APIRequestContext):
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


def test_login_success(api_request_context: APIRequestContext):
    response = api_request_context.post(
        "/api/login",
        data={"email": "eve.holt@reqres.in", "password": "cityslicka"},
    )

    assert response.status == 200

    body = LoginResponse.model_validate(response.json())

    assert body.token  # 只要 token 不是 None 或空字串，就會通過
