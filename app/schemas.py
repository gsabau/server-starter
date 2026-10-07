from dataclasses import dataclass


# Request and response shapes. A dataclass, fields only.
# The stored rows live in app/domain/models.py.
# A cell is "", "X", or "O". A board is nine cells, index 0 to 8, row by row.


@dataclass
class UserCreate:
    # Body for a new account. The client does not send the id.
    name: str


@dataclass
class UserResponse:
    # Account returned to the client.
    id: int
    name: str


@dataclass
class ProfileCreate:
    # Public face. One profile per user.
    user_id: int
    display_name: str


@dataclass
class ProfileResponse:
    # Profile returned to the client.
    id: int
    user_id: int
    display_name: str


@dataclass
class GameCreate:
    # Seats two different users in one browser. The client sends both ids.
    player_x_user_id: int
    player_o_user_id: int


@dataclass
class GameResponse:
    # Board the client draws. next is "X" or "O", or None when the game is over.
    # status is in_progress, x_wins, o_wins, or draw.
    id: int
    board: list[str]
    next: str | None
    status: str
    player_x_user_id: int
    player_o_user_id: int


@dataclass
class MoveCreate:
    # One mark. cell is 0 to 8. The mark is whoever next says, not a field here.
    cell: int


@dataclass
class ScoreHistoryResponse:
    # One finished game for one user. A game writes two rows, one per player.
    # result is win, loss, or draw. Wins are counted from these rows.
    id: int
    game_id: int
    user_id: int
    opponent_user_id: int
    result: str
    played_at: str
