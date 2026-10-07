from app.domain.models import Score
from app.scores.repository import ScoreRepository


class ScoreService:
    """Reads the history. The game service writes the rows."""

    def __init__(self, repository: ScoreRepository):
        self._repository = repository

    def list_scores(self) -> list[Score]:
        return self._repository.list_all()
