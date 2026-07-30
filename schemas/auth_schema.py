from pydantic import BaseModel, ConfigDict

# reqres.in /api/login 相關 API 回應的型別定義。
# extra="ignore"：回應裡多出未定義的欄位就忽略，不會因為 API 新增欄位而測試失敗，
# 但少了必要欄位或型態不符時，model_validate() 仍會拋出 ValidationError。


class LoginResponse(BaseModel):
    """POST /api/login 成功時的回應（帳密正確）"""

    model_config = ConfigDict(extra="ignore")

    token: str


class ErrorResponse(BaseModel):
    """POST /api/login 失敗時的回應（例如缺少密碼）"""

    model_config = ConfigDict(extra="ignore")

    error: str
