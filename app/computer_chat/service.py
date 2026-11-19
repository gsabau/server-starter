import logging
from collections.abc import AsyncIterable

from pydantic_ai import Agent
from pydantic_ai.messages import FunctionToolCallEvent, FunctionToolResultEvent
from pydantic_ai.usage import UsageLimits

from app.computer_chat.tools import ChatContext
from app.game_histories.service import GameHistoryService
from app.profiles.service import ProfileService
from app.users.service import UserService

logger = logging.getLogger("app.computer_chat")

MAX_MODEL_REQUESTS = 6


class ComputerChatService:
    """Logic layer. Runs the chat agent with access to game services and returns its text reply.
    Does not know HTTP."""

    def __init__(
        self,
        chat_agent: Agent[ChatContext, str],
        user_service: UserService,
        profile_service: ProfileService,
        history_service: GameHistoryService,
    ):
        self._chat_agent = chat_agent
        self._user_service = user_service
        self._profile_service = profile_service
        self._history_service = history_service

    async def ask(self, text: str) -> str:
        logger.info("ask text=%r", text)
        chat_context = ChatContext(
            user_service=self._user_service,
            profile_service=self._profile_service,
            history_service=self._history_service,
        )
        result = await self._chat_agent.run(
            text,
            deps=chat_context,
            usage_limits=UsageLimits(request_limit=MAX_MODEL_REQUESTS),
            event_stream_handler=_log_model_events,
        )
        logger.info("reply=%r", result.output)
        return result.output


async def _log_model_events(_context, events: AsyncIterable[object]) -> None:
    """One line per function call, and one for the text the function gave back.

    A tool added in tools.py shows up here without a log line of its own.
    """
    async for event in events:
        if isinstance(event, FunctionToolCallEvent):
            logger.info("tool call %s %s", event.part.tool_name, event.part.args)
        elif isinstance(event, FunctionToolResultEvent):
            logger.info("tool result %s: %s", event.part.tool_name, event.part.model_response_str())
