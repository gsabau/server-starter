from datetime import datetime, timezone

from app.domain.models import Game
from app.games.repository import GameRepository
from app.scores.repository import ScoreRepository
from app.users.repository import UserRepository

# Three rows, three columns, two diagonals. Index 0 is the top left.
LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


class UnknownUserError(Exception):
    pass


class SameUserError(Exception):
    pass


class GameNotFoundError(Exception):
    pass


class IllegalMoveError(Exception):
    def __init__(self, detail: str):
        self.detail = detail


class GameService:
    """Board rules. The mark comes from next. Does not know HTTP."""

    def __init__(self, games: GameRepository, users: UserRepository, scores: ScoreRepository):
        self._games = games
        self._users = users
        self._scores = scores

    def create_game(self, player_x_user_id: int, player_o_user_id: int) -> Game:
        if player_x_user_id == player_o_user_id:
            raise SameUserError
        if self._users.get(player_x_user_id) is None or self._users.get(player_o_user_id) is None:
            raise UnknownUserError
        return self._games.add(player_x_user_id, player_o_user_id)

    def list_games(self) -> list[Game]:
        return self._games.list_all()

    def get_game(self, game_id: int) -> Game:
        game = self._games.get(game_id)
        if game is None:
            raise GameNotFoundError
        return game

    def move(self, game_id: int, cell: int) -> Game:
        game = self.get_game(game_id)
        if game.status != "in_progress" or game.next is None:
            raise IllegalMoveError("Game is over")
        if cell < 0 or cell > 8:
            raise IllegalMoveError("Cell is out of range")
        if game.board[cell] != "":
            raise IllegalMoveError("Cell is taken")

        mark = game.next
        game.board[cell] = mark
        if _has_line(game.board, mark):
            game.status = "x_wins" if mark == "X" else "o_wins"
            game.next = None
            self._record(game)
        elif all(entry != "" for entry in game.board):
            game.status = "draw"
            game.next = None
            self._record(game)
        else:
            game.next = "O" if mark == "X" else "X"
        return game

    def _record(self, game: Game) -> None:
        if game.status == "x_wins":
            x_result, o_result = "win", "loss"
        elif game.status == "o_wins":
            x_result, o_result = "loss", "win"
        else:
            x_result, o_result = "draw", "draw"
        played_at = datetime.now(timezone.utc).isoformat()
        self._scores.add(game.id, game.player_x_user_id, game.player_o_user_id, x_result, played_at)
        self._scores.add(game.id, game.player_o_user_id, game.player_x_user_id, o_result, played_at)


def _has_line(board: list[str], mark: str) -> bool:
    return any(board[a] == mark and board[b] == mark and board[c] == mark for a, b, c in LINES)
