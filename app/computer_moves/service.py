from pydantic_ai import Agent
from pydantic_ai.usage import UsageLimits

from app.computer_moves.tools import GameContext

MAX_MODEL_REQUESTS = 6  # one move, plus a few retries after a taken position


class ComputerMoveService:
    """Logic layer. Lets the agent move and returns the position the move tool recorded.
    Does not know HTTP."""

    def __init__(self, agent: Agent[GameContext, str]):
        self._agent = agent

    async def choose_move(self, game: list[str], mark: str) -> int:
        game_context = GameContext(board=list(game), mark=mark)
        await self._agent.run(
            _describe_board(game, mark),
            deps=game_context,
            usage_limits=UsageLimits(request_limit=MAX_MODEL_REQUESTS),
        )
        return game_context.move


def _describe_board(game: list[str], mark: str) -> str:
    # Free cells show their position, taken cells show X or O.
    cells = [cell or str(index) for index, cell in enumerate(game)]
    rows = [" | ".join(cells[start : start + 3]) for start in (0, 3, 6)]
    return "\n".join(rows) + f"\n\nYou play {mark}. Make your move."
