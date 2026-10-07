from dataclasses import dataclass


# Rows the repositories store. The dict stands in for the database.
# A dataclass, fields only.


@dataclass
class User:
    # Account. id and name.
    id: int
    name: str


@dataclass
class Profile:
    # Public face. One profile per user.
    id: int
    user_id: int
    display_name: str


@dataclass
class Game:
    # Board of nine cells, index 0 to 8, row by row. A cell is "", "X", or "O".
    # next is "X" or "O", or None when the game is over.
    # status is in_progress, x_wins, o_wins, or draw.
    id: int
    board: list[str]
    next: str | None
    status: str
    player_x_user_id: int
    player_o_user_id: int


@dataclass
class Score:
    # One finished game for one user. A game writes two rows, one per player.
    # result is win, loss, or draw.
    id: int
    game_id: int
    user_id: int
    opponent_user_id: int
    result: str
    played_at: str
