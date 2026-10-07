from app.domain.models import User


class UserRepository:
    """Data layer. The dict stands in for the database."""

    def __init__(self):
        self._users: dict[int, User] = {}
        self._next_id = 1

    def add(self, name: str) -> User:
        user = User(id=self._next_id, name=name)
        self._users[user.id] = user
        self._next_id += 1
        return user

    def get(self, user_id: int) -> User | None:
        return self._users.get(user_id)

    def list_all(self) -> list[User]:
        return list(self._users.values())
