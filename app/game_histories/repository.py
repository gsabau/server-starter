from app.domain.models import GameHistory


class GameHistoryRepository:
    """Data layer. The dict holds the finished games. The key is the id as text."""

    def __init__(self):
        self._histories: dict[str, GameHistory] = {}
        self._next_id = 1

    def add(self, player_a: str, player_b: str, game: list[str], winner: str) -> GameHistory:
        history = GameHistory(
            id=str(self._next_id),
            player_a=player_a,
            player_b=player_b,
            game=list(game),
            winner=winner,
        )
        self._histories[history.id] = history
        self._next_id += 1
        return history

    def get(self, history_id: str) -> GameHistory | None:
        return self._histories.get(history_id)

    def list_all(self) -> list[GameHistory]:
        return list(self._histories.values())
