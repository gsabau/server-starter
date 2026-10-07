from app.domain.models import Score


class ScoreRepository:
    """Data layer. Two rows per finished game, one per player."""

    def __init__(self):
        self._scores: dict[int, Score] = {}
        self._next_id = 1

    def add(self, game_id: int, user_id: int, opponent_user_id: int, result: str, played_at: str) -> Score:
        score = Score(
            id=self._next_id,
            game_id=game_id,
            user_id=user_id,
            opponent_user_id=opponent_user_id,
            result=result,
            played_at=played_at,
        )
        self._scores[score.id] = score
        self._next_id += 1
        return score

    def list_all(self) -> list[Score]:
        return list(self._scores.values())
