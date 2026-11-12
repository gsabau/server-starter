from typing import Annotated

from fastapi import APIRouter, HTTPException, Path

from app.domain.models import GameHistory
from app.game_histories.service import GameHistoryNotFoundError, GameHistoryService, InvalidGameHistoryError
from app.schemas import GameHistoryCreate, GameHistoryResponse


def build_router(service: GameHistoryService) -> APIRouter:
    """Presentation layer. One finished game per entry. The client plays, the server stores."""

    router = APIRouter(prefix="/game-histories", tags=["game-histories"])

    @router.post("", status_code=201)
    def create_history(body: GameHistoryCreate) -> GameHistoryResponse:
        return _to_response(
            _run(lambda: service.create_history(body.player_a, body.player_b, body.game, body.winner))
        )

    @router.get("")
    def list_histories() -> list[GameHistoryResponse]:
        return [_to_response(history) for history in service.list_histories()]

    @router.get("/{history_id}")
    def get_history(
        history_id: Annotated[
            str,
            Path(description='Id des Eintrags als Text, zum Beispiel "1". Unbekannte Id: 404.', examples=["1"]),
        ],
    ) -> GameHistoryResponse:
        return _to_response(_run(lambda: service.get_history(history_id)))

    return router


def _run(action):
    try:
        return action()
    except GameHistoryNotFoundError:
        raise HTTPException(status_code=404, detail="Game history not found")
    except InvalidGameHistoryError as error:
        raise HTTPException(status_code=400, detail=error.detail)


def _to_response(history: GameHistory) -> GameHistoryResponse:
    return GameHistoryResponse(
        id=history.id,
        player_a=history.player_a,
        player_b=history.player_b,
        game=list(history.game),
        winner=history.winner,
    )
