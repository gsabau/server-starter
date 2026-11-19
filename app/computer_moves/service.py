import logging
from collections.abc import AsyncIterable

from pydantic_ai import Agent
from pydantic_ai.messages import FunctionToolCallEvent, FunctionToolResultEvent
from pydantic_ai.usage import UsageLimits

from app.computer_moves.tools import GameContext

logger = logging.getLogger("app.computer_moves")

MAX_MODEL_REQUESTS = 6  # one move, plus a few retries after a taken position


class ComputerMoveService:
    """Logic layer. Lets the agent move and returns the position the move tool recorded.
    Does not know HTTP."""

    def __init__(self, game_agent: Agent[GameContext, str]):
        self._game_agent = game_agent

    async def choose_move(self, game: list[str], mark: str) -> int:
        logger.info("choose_move mark=%s", mark)
        prompt = _describe_board(game, mark)
        logger.info("prompt:\n%s", prompt)
        game_context = GameContext(board=list(game), mark=mark)
        result = await self._game_agent.run(
            prompt,
            deps=game_context,
            usage_limits=UsageLimits(request_limit=MAX_MODEL_REQUESTS),
            event_stream_handler=_log_model_events,
        )
        logger.info("result=%s", result)
        logger.info("choose_move position=%s", game_context.move)
        return game_context.move


async def _log_model_events(_context, events: AsyncIterable[object]) -> None:
    """One line per function call, and one for the text the function gave back.

    A tool added in tools.py shows up here without a log line of its own.
    """
    async for event in events:
        if isinstance(event, FunctionToolCallEvent):
            logger.info("tool call %s %s", event.part.tool_name, event.part.args)
        elif isinstance(event, FunctionToolResultEvent):
            logger.info("tool result %s: %s", event.part.tool_name, event.part.model_response_str())


def _describe_board(game: list[str], mark: str) -> str:
    """Turn the board into the text the model reads.

    A free cell shows its position (0 to 8), a taken cell shows X or O.
    The last line names the mark the computer plays.

    Example for game=["X", "O", "", "", "X", "", "", "", "O"] and mark="O":

        X | O | 2
        3 | X | 5
        6 | 7 | O

        You play O. Make your move.
    """
    cells = [cell or str(index) for index, cell in enumerate(game)]
    rows = [" | ".join(cells[start : start + 3]) for start in (0, 3, 6)]
    return "\n".join(rows) + f"\n\nYou play {mark}. Make your move."
