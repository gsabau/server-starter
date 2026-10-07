from app.domain.models import Profile
from app.profiles.repository import ProfileRepository
from app.users.repository import UserRepository


class UnknownUserError(Exception):
    pass


class ProfileExistsError(Exception):
    pass


class ProfileService:
    """One public face per account. Does not know HTTP."""

    def __init__(self, profiles: ProfileRepository, users: UserRepository):
        self._profiles = profiles
        self._users = users

    def create_profile(self, user_id: int, display_name: str) -> Profile:
        if self._users.get(user_id) is None:
            raise UnknownUserError
        if self._profiles.find_by_user(user_id) is not None:
            raise ProfileExistsError
        return self._profiles.add(user_id, display_name)

    def list_profiles(self) -> list[Profile]:
        return self._profiles.list_all()
