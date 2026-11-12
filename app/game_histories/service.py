from app.domain.models import GameHistory
from app.game_histories.repository import GameHistoryRepository

DRAW = "draw"
CELLS = ("", "X", "O")


class GameHistoryNotFoundError(Exception):
    pass


class InvalidGameHistoryError(Exception):
    def __init__(self, detail: str):
        self.detail = detail


class GameHistoryService:
    """Logic layer. Checks a finished game before it is stored. Does not know HTTP."""

    def __init__(self, repository: GameHistoryRepository):
        self._repository = repository

    def create_history(self, player_a: str, player_b: str, game: list[str], winner: str) -> GameHistory:
        player_a = player_a.strip()
        player_b = player_b.strip()
        winner = winner.strip()
        if not player_a or not player_b:
            raise InvalidGameHistoryError("Player name is empty")
        if player_a == player_b:
            raise InvalidGameHistoryError("Players must differ")
        if len(game) != 9:
            raise InvalidGameHistoryError("Game must have nine cells")
        if any(cell not in CELLS for cell in game):
            raise InvalidGameHistoryError("Cell must be empty, X, or O")
        if winner not in (player_a, player_b, DRAW):
            raise InvalidGameHistoryError("Winner must be a player or draw")
        return self._repository.add(player_a, player_b, game, winner)

    def list_histories(self) -> list[GameHistory]:
        return self._repository.list_all()

    def get_history(self, history_id: str) -> GameHistory:
        history = self._repository.get(history_id)
        if history is None:
            raise GameHistoryNotFoundError
        return history
