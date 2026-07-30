from pydantic import BaseModel, ConfigDict

# reqres.in /api/users 相關 API 回應的型別定義。


class User(BaseModel):
    """使用者列表中單一筆使用者資料"""

    model_config = ConfigDict(extra="ignore")

    id: int
    email: str
    first_name: str
    last_name: str
    avatar: str


class SupportInfo(BaseModel):
    """回應中附帶的 reqres.in 官方支援資訊區塊（與業務邏輯無關，但屬於回應結構的一部分）"""

    model_config = ConfigDict(extra="ignore")

    url: str
    text: str


class UsersListResponse(BaseModel):
    """GET /api/users 的分頁列表回應，巢狀組合 User 與 SupportInfo"""

    model_config = ConfigDict(extra="ignore")

    page: int
    per_page: int
    total: int
    total_pages: int
    data: list[User]
    support: SupportInfo


class CreateUserResponse(BaseModel):
    """POST /api/users 建立成功後的回應，包含伺服器自動產生的 id 與 createdAt"""

    model_config = ConfigDict(extra="ignore")

    name: str
    job: str
    id: str
    createdAt: str
