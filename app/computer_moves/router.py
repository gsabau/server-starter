from fastapi import APIRouter

from app.computer_moves.service import ComputerMoveService
from app.schemas import ComputerMoveRequest, ComputerMoveResponse


def build_router(service: ComputerMoveService) -> APIRouter:
    """Presentation layer. The app sends the board, an agent picks the move, the app plays it. Nothing is stored."""

    router = APIRouter(prefix="/computer-moves", tags=["computer"])

    @router.post("")
    async def request_computer_move(body: ComputerMoveRequest) -> ComputerMoveResponse:
        position = await service.choose_move(body.game, body.mark)
        return ComputerMoveResponse(position=position)

    return router

