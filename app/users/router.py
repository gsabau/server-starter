from fastapi import APIRouter, HTTPException

from app.domain.models import User
from app.schemas import UserCreate, UserResponse
from app.users.service import EmptyNameError, UserService


def build_router(service: UserService) -> APIRouter:
    """Presentation layer. Calls the service. Does not know the dict."""

    router = APIRouter(prefix="/users", tags=["users"])

    @router.post("", status_code=201)
    def create_user(body: UserCreate) -> UserResponse:
        return _to_response(_run(lambda: service.create_user(body.name)))

    @router.get("")
    def list_users() -> list[UserResponse]:
        return [_to_response(user) for user in service.list_users()]

    return router


def _run(action):
    try:
        return action()
    except EmptyNameError:
        raise HTTPException(status_code=400, detail="Name is empty")


# User and UserResponse have the same two fields. The mapping is the boundary
# between the app and the HTTP response. User lives in app/domain/models.py.
# The repository and the service pass that row around. Those layers do not
# know JSON. UserResponse is the shape FastAPI turns into JSON and into the
# OpenAPI page. UserCreate is a different shape: only name, because the client
# does not send the id.
def _to_response(user: User) -> UserResponse:
    return UserResponse(id=user.id, name=user.name)
