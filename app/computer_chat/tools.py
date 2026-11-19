from dataclasses import dataclass

from pydantic_ai import RunContext

from app.game_histories.service import GameHistoryService
from app.profiles.service import ProfileService
from app.users.service import UserService

# The function calls of the chat agent. This is the file you extend.
#
# The model never sees the Python code. It only sees a schema built from three things:
#   1. the function name (verb + object),
#   2. the parameters (name, type),
#   3. the docstring (what the function is for, and when to use it — never how).
#
# A new function call = one function here + one entry in TOOLS below.
# Ideas: list_game_histories, get_high_scores.


@dataclass
class ChatContext:
    user_service: UserService
    profile_service: ProfileService
    history_service: GameHistoryService


def list_users(ctx: RunContext[ChatContext]) -> str:
    """List all registered users with their id and name. Use this when asked about players or users."""
    users = ctx.deps.user_service.list_users()
    if not users:
        return "No users found."
    return "\n".join(f"id={user.id}, name={user.name}" for user in users)


TOOLS = [list_users]
