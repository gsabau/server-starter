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
class GameHistory:
    # One finished game, as the client reports it.
    # game is nine cells, index 0 to 8, row by row. A cell is "", "X", or "O".
    # player_a plays X, player_b plays O.
    # winner is the name of player_a or player_b, or "draw".
    id: str
    player_a: str
    player_b: str
    game: list[str]
    winner: str
