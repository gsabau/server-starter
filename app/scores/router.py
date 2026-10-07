from fastapi import APIRouter

from app.domain.models import Score
from app.schemas import ScoreHistoryResponse
from app.scores.service import ScoreService


def build_router(service: ScoreService) -> APIRouter:
    router = APIRouter(prefix="/scores", tags=["scores"])

    @router.get("")
    def list_scores() -> list[ScoreHistoryResponse]:
        return [_to_response(score) for score in service.list_scores()]

    return router


def _to_response(score: Score) -> ScoreHistoryResponse:
    return ScoreHistoryResponse(
        id=score.id,
        game_id=score.game_id,
        user_id=score.user_id,
        opponent_user_id=score.opponent_user_id,
        result=score.result,
        played_at=score.played_at,
    )
