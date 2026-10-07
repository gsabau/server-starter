from app.domain.models import Game


class GameRepository:
    """Data layer. The dict holds the board the service updates."""

    def __init__(self):
        self._games: dict[int, Game] = {}
        self._next_id = 1

    def add(self, player_x_user_id: int, player_o_user_id: int) -> Game:
        game = Game(
            id=self._next_id,
            board=[""] * 9,
            next="X",
            status="in_progress",
            player_x_user_id=player_x_user_id,
            player_o_user_id=player_o_user_id,
        )
        self._games[game.id] = game
        self._next_id += 1
        return game

    def get(self, game_id: int) -> Game | None:
        return self._games.get(game_id)

    def list_all(self) -> list[Game]:
        return list(self._games.values())
