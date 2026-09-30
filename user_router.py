from fastapi import APIRouter, HTTPException

from domain.models import User
from dtos.dtos import UserCreate, UserResponse
from user_service import EmptyNameError, UserService


def build_router(service: UserService) -> APIRouter:
    """Presentation layer. One route. Calls the service."""

    router = APIRouter(prefix="/users", tags=["users"])

    @router.post("", status_code=201)
    def create_user(body: UserCreate) -> UserResponse:
        return _to_response(_run(lambda: service.create_user(body.name)))

    return router


def _run(action):
    try:
        return action()
    except EmptyNameError:
        raise HTTPException(status_code=400, detail="Name is empty")


# User and UserResponse have the same two fields. The mapping is the boundary
# between the app and the HTTP response. User lives in domain/models.py. The
# repository and the service pass that row around. Those layers do not know
# JSON. UserResponse is the DTO FastAPI turns into JSON and into the OpenAPI
# page. UserCreate is a different shape: only name, because the client does
# not send the id.
def _to_response(user: User) -> UserResponse:
    return UserResponse(id=user.id, name=user.name)
