# Frontend

Zwei Personen, ein Browser. Die Seite zeigt die Spieler, startet ein Spiel, zeichnet das Brett und schickt jeden Klick als Zug. Der Server entscheidet das Zeichen, den Sieg und die Score-Zeilen.

Der Server hört auf `http://127.0.0.1:8000`. Die React-App hört auf `http://127.0.0.1:5173` oder `http://localhost:5173`. Diese Origins darf der Browser aufrufen. `../client-starter` zeigt schon die User-Liste. Dort das Spiel weiterbauen.

Die Beschreibung zum Ausprobieren ist [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). Die Datei dazu ist [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json). Im Ordner der React-App:

```powershell
npx @openapitools/openapi-generator-cli generate -i http://127.0.0.1:8000/openapi.json -g typescript-axios -o client-node
```

Node.js und Java. `axios` ist eine Abhängigkeit der App. Eine `Configuration` für alle vier Klassen:

```typescript
import { Configuration, GamesApi, ProfilesApi, ScoresApi, UsersApi } from "./client-node";

const config = new Configuration({ basePath: "http://127.0.0.1:8000" });
const users = new UsersApi(config);
const profiles = new ProfilesApi(config);
const games = new GamesApi(config);
const scores = new ScoresApi(config);
```

## Wo welcher Aufruf hingehört

| Moment | Aufruf | Danach |
|---|---|---|
| Seite öffnet, Sitzplätze | `GET /users`, `GET /profiles` | Namen an die beiden Plätze X und O |
| Jemand ist neu | `POST /users`, dann `POST /profiles` | Die neue Id an einen Platz |
| Liste der Partien, Lobby | `GET /games` | Laufende und beendete Bretter |
| Partie öffnen | `GET /games/{game_id}` | Neun Felder zeichnen |
| Neue Partie | `POST /games` | Die Antwort ist das leere Brett. Diese `id` öffnen |
| Klick auf ein leeres Feld | `POST /games/{game_id}/moves` | Die Antwort ersetzt das Brett. Kein zweites Laden nötig |
| Partie zu Ende, Verlauf | `GET /scores` | Zwei neue Zeilen. Siege sind die Zeilen mit `result` `"win"` |

Ein Zug schickt keine User-Id und kein `"X"` oder `"O"`. Der Server setzt, wen `next` nennt. Beide Personen klicken im selben Fenster. Die Seite zeigt nur an, wer dran ist.

## Spiel

### Sitzplätze

`GET /users` liefert die Konten. `GET /profiles` liefert den Namen, der am Platz steht. `user_id` im Profil ist `id` beim User. Beim Start:

| User | Name | Profil |
|---|---|---|
| 1 | Ada | Ada |
| 2 | Ben | Ben |
| 3 | Cleo | Cleo |
| 4 | Dan | Dan |

Die Seite merkt sich zwei Ids. Eine ist X, eine ist O. Sie müssen verschieden sein.

Ein neuer Mensch: zuerst `POST /users` mit `{ "name": "Eve" }`. Die Antwort ist `{"id": 5, "name": "Eve"}`. Danach `POST /profiles` mit `{ "user_id": 5, "display_name": "Eve" }`. Ohne Profil gibt es den Menschen trotzdem. Das Profil ist nur der angezeigte Name. Ein zweites Profil für dieselbe Id ist **400**.

### Partie starten

`POST /games` mit den beiden Ids:

```json
{"player_x_user_id": 1, "player_o_user_id": 2}
```

**201.** Die Antwort ist das Brett, auf dem sofort gespielt wird:

```json
{
  "id": 6,
  "board": ["", "", "", "", "", "", "", "", ""],
  "next": "X",
  "status": "in_progress",
  "player_x_user_id": 1,
  "player_o_user_id": 2
}
```

`id` 6, weil 1 bis 5 schon aus den Testdaten stammen. X beginnt. Beide Ids müssen existieren.

Wer nicht neu anlegen will, öffnet Spiel 2. Cleo ist X, Dan ist O, das Brett ist leer.

### Brett

`GET /games/{game_id}` oder die Antwort von `POST /games`. Neun Felder, Zeile für Zeile:

```
0 1 2
3 4 5
6 7 8
```

Ein Feld ist `""`, `"X"` oder `"O"`. `player_x_user_id` ist der Mensch hinter X, `player_o_user_id` hinter O. Die Namen kommen aus `GET /users` oder `GET /profiles`.

`next` ist `"X"` oder `"O"`, solange `status` `in_progress` ist. Die Seite schreibt darüber, wer dran ist. Leere Felder sind klickbar. Belegte nicht.

Spiel 1 ist mitten in der Partie. Ada ist X, Ben ist O, O ist dran:

```json
{
  "id": 1,
  "board": ["X", "O", "", "", "X", "", "", "", ""],
  "next": "O",
  "status": "in_progress",
  "player_x_user_id": 1,
  "player_o_user_id": 2
}
```

`status` ist `in_progress`, `x_wins`, `o_wins` oder `draw`. Bei den letzten drei ist `next` `null`. Keine Felder mehr klickbar. Spiel 3 ist ein Sieg von X, Spiel 4 ein Sieg von O, Spiel 5 unentschieden.

### Zug

Klick auf Feld `cell`. Nur diese Zahl geht an den Server:

```json
{"cell": 0}
```

`POST /games/2/moves`. Die Antwort ist das ganze Brett nach dem Zug. Feld 0 ist `"X"`, `next` ist `"O"`. Diese JSON zeichnet die Seite neu. Sie ruft `GET /games/2` dafür nicht noch einmal auf.

Der nächste Klick, zum Beispiel Feld 4, ist wieder nur `{ "cell": 4 }`. Der Server setzt `"O"`, weil `next` jetzt `"O"` war. So geht es weiter, abwechselnd, im selben Fenster.

Drei Fälle beenden die Partie. Drei gleiche Zeichen in einer Zeile, einer Spalte oder einer Diagonale: `status` wird `x_wins` oder `o_wins`. Ein volles Brett ohne Linie: `status` wird `draw`. Dann ist `next` `null`, und der Server schreibt zwei Score-Zeilen. Die Zug-Antwort enthält das Brett, nicht die Score-Zeilen.

Ein Zug auf ein beendetes Spiel, auf ein Feld außerhalb 0–8 oder auf ein belegtes Feld ist **400**. Das Brett bleibt, wie es war.

### Verlauf

Nach einem Ende, und wenn die Lobby die Siege zeigt: `GET /scores`. Ein beendetes Spiel hat zwei Zeilen, eine pro Person. Dieselbe `played_at`, dieselbe `game_id`.

Spiel 3, Ada (X) hat gegen Cleo gewonnen. Die ersten beiden Zeilen nach dem Start:

```json
[
  {
    "id": 1,
    "game_id": 3,
    "user_id": 1,
    "opponent_user_id": 3,
    "result": "win",
    "played_at": "2026-10-07T09:00:00+00:00"
  },
  {
    "id": 2,
    "game_id": 3,
    "user_id": 3,
    "opponent_user_id": 1,
    "result": "loss",
    "played_at": "2026-10-07T09:00:00+00:00"
  }
]
```

`result` ist `win`, `loss` oder `draw`. `played_at` ist die Uhrzeit des Serverstarts, ISO-Format. Siege von Ada sind die Zeilen mit `user_id` 1 und `result` `"win"`. Es gibt keinen zweiten Aufruf dafür.

Spiele 3, 4 und 5 sind schon zu Ende. `GET /scores` liefert dafür sechs Zeilen, bevor jemand selbst spielt.

## Endpoints

### `GET /users`

Lobby, Sitzplätze. `users.listUsersUsersGet()`.

**200.** Liste von `UserResponse`: `id`, `name`.

### `POST /users`

Neuer Mensch, bevor er einen Platz bekommt. `users.createUserUsersPost({ name })`.

Body `UserCreate`: `name`. Die Id schickt die Seite nicht.

**201.** `UserResponse`. Die nächste Id nach den Testdaten ist 5.

**400.** `Name is empty`, wenn der Name leer oder nur Leerzeichen ist.

### `GET /profiles`

Anzeigename am Sitzplatz. `profiles.listProfilesProfilesGet()`.

**200.** Liste von `ProfileResponse`: `id`, `user_id`, `display_name`. Ein Profil pro User.

### `POST /profiles`

Anzeigename für einen vorhandenen User. `profiles.createProfileProfilesPost({ user_id, display_name })`.

Body `ProfileCreate`: `user_id`, `display_name`.

**201.** `ProfileResponse`.

**404.** `User not found`.

**400.** `Profile already exists`.

### `GET /games`

Lobby. `games.listGamesGamesGet()`.

**200.** Liste von `GameResponse`. Felder unten bei `GET /games/{game_id}`.

### `POST /games`

Neue Partie, nachdem zwei verschiedene User sitzen. `games.createGameGamesPost({ player_x_user_id, player_o_user_id })`.

Body `GameCreate`: `player_x_user_id`, `player_o_user_id`.

**201.** `GameResponse`. Leeres Brett, `next` ist `"X"`, `status` ist `in_progress`.

**400.** `Users must differ`.

**404.** `User not found`.

### `GET /games/{game_id}`

Partie öffnen. `games.getGameGamesGameIdGet(gameId)`.

**200.** `GameResponse`:

| Feld | Bedeutung |
|---|---|
| `id` | Partie |
| `board` | Neun Strings, Index 0–8. `""`, `"X"` oder `"O"` |
| `next` | `"X"` oder `"O"`. `null`, wenn die Partie zu Ende ist |
| `status` | `in_progress`, `x_wins`, `o_wins`, `draw` |
| `player_x_user_id` | User, der X spielt |
| `player_o_user_id` | User, der O spielt |

**404.** `Game not found`.

### `POST /games/{game_id}/moves`

Klick auf ein Feld. `games.moveGamesGameIdMovesPost(gameId, { cell })`.

Body `MoveCreate`: nur `cell`, eine Zahl 0–8.

**200.** `GameResponse`, das Brett nach dem Zug. Bei Sieg oder Remis ist `next` `null`. Zwei Score-Zeilen entstehen dabei, stehen aber in `GET /scores`.

**400.** `Game is over`, `Cell is out of range`, `Cell is taken`.

**404.** `Game not found`.

### `GET /scores`

Verlauf, nachdem eine Partie `in_progress` verlassen hat. Auch für die Siegeszahl in der Lobby. `scores.listScoresScoresGet()`.

**200.** Liste von `ScoreHistoryResponse`:

| Feld | Bedeutung |
|---|---|
| `id` | Zeile |
| `game_id` | Partie. Zwei Zeilen teilen sich diese Id |
| `user_id` | Diese Person |
| `opponent_user_id` | Die andere Person |
| `result` | `win`, `loss` oder `draw` |
| `played_at` | ISO-Zeitpunkt. Beide Zeilen einer Partie gleich |

Ein Sieg von X schreibt `win` für `player_x_user_id` und `loss` für `player_o_user_id`. Ein Sieg von O ist umgekehrt. Ein Remis schreibt zweimal `draw`.
