from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    email: str
    first_name: str
    last_name: str
    avatar: str


class SupportInfo(BaseModel):
    model_config = ConfigDict(extra="ignore")

    url: str
    text: str


class UsersListResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    page: int
    per_page: int
    total: int
    total_pages: int
    data: list[User]
    support: SupportInfo


class CreateUserResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str
    job: str
    id: str
    createdAt: str
