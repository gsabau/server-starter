from app.domain.models import Profile


class ProfileRepository:
    """Data layer. One dict. The key is the profile id."""

    def __init__(self):
        self._profiles: dict[int, Profile] = {}
        self._next_id = 1

    def add(self, user_id: int, display_name: str) -> Profile:
        profile = Profile(id=self._next_id, user_id=user_id, display_name=display_name)
        self._profiles[profile.id] = profile
        self._next_id += 1
        return profile

    def find_by_user(self, user_id: int) -> Profile | None:
        for profile in self._profiles.values():
            if profile.user_id == user_id:
                return profile
        return None

    def list_all(self) -> list[Profile]:
        return list(self._profiles.values())
