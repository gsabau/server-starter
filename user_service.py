from domain.models import User
from user_repository import UserRepository


class EmptyNameError(Exception):
    pass


class UserService:
    """Logic layer. Knows the rules. Does not know HTTP."""

    def __init__(self, repository: UserRepository):
        self._repository = repository

    def create_user(self, name: str) -> User:
        if not name.strip():
            raise EmptyNameError
        return self._repository.add(name.strip())
