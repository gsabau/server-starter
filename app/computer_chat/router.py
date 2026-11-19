from fastapi import APIRouter

from app.computer_chat.service import ComputerChatService
from app.schemas import ComputerChatRequest, ComputerChatResponse


def build_router(service: ComputerChatService) -> APIRouter:
    """Presentation layer. The app sends a question, the chat agent answers it. Nothing is stored."""

    router = APIRouter(prefix="/computer-chat", tags=["computer"])

    @router.post("")
    async def request_computer_chat(body: ComputerChatRequest) -> ComputerChatResponse:
        reply = await service.ask(body.text)
        return ComputerChatResponse(reply=reply)

    return router
