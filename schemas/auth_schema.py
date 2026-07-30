from pydantic import BaseModel, ConfigDict


class LoginResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    token: str


class ErrorResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    error: str
