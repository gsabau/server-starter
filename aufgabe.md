# Aufgabe

Dieselbe Architektur wie `POST /users`. Repository, Service, Router. Die DTOs sind schon in `dtos/dtos.py`. `User` steht in `domain/models.py`.

1. Profil anlegen und lesen. `POST /profiles` mit `ProfileCreate`. `GET /profiles`.
2. User lesen. `GET /users`.
3. Spiel anlegen und lesen. `POST /games` mit `GameCreate`. Zwei verschiedene User. `GET /games` und `GET /games/{game_id}`.
4. Zug. `POST /games/{game_id}/moves` mit `MoveCreate`. Feld `0` bis `8`. Abweisen, wenn das Spiel zu Ende ist, der falsche Spieler dran ist, oder das Feld belegt ist. Am Ende zwei Zeilen `ScoreHistoryResponse`, eine pro User.
5. Verlauf. `GET /scores`. Gewonnen, verloren und unentschieden aus diesen Zeilen zählen.
