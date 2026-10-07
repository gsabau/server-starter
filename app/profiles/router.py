from fastapi import APIRouter, HTTPException

from app.domain.models import Profile
from app.profiles.service import ProfileExistsError, ProfileService, UnknownUserError
from app.schemas import ProfileCreate, ProfileResponse


def build_router(service: ProfileService) -> APIRouter:
    router = APIRouter(prefix="/profiles", tags=["profiles"])

    @router.post("", status_code=201)
    def create_profile(body: ProfileCreate) -> ProfileResponse:
        return _to_response(_run(lambda: service.create_profile(body.user_id, body.display_name)))

    @router.get("")
    def list_profiles() -> list[ProfileResponse]:
        return [_to_response(profile) for profile in service.list_profiles()]

    return router


def _run(action):
    try:
        return action()
    except UnknownUserError:
        raise HTTPException(status_code=404, detail="User not found")
    except ProfileExistsError:
        raise HTTPException(status_code=400, detail="Profile already exists")


def _to_response(profile: Profile) -> ProfileResponse:
    return ProfileResponse(
        id=profile.id,
        user_id=profile.user_id,
        display_name=profile.display_name,
    )
