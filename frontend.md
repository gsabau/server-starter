# Frontend

Zwei Personen, ein Browser. Die Seite zeigt die Spieler, zeichnet das Brett und erkennt selbst, wer gewinnt. Der Server entscheidet nichts im Spiel. Er speichert nur das fertige Spiel als Verlauf.

Der Server hört auf `http://127.0.0.1:8000`. Die React-App hört auf `http://127.0.0.1:5173` oder `http://localhost:5173`. Diese Origins darf der Browser aufrufen. Läuft deine App woanders (Vite nimmt 5174, wenn 5173 belegt ist), trag die Adresse in `main.py` bei `allow_origins` ein. Siehe Abschnitt CORS unten. `../client-starter` zeigt schon die User-Liste und das lokale Brett. Dort das Spiel weiterbauen.

Die Beschreibung zum Ausprobieren ist [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). Dort steht zu jedem Feld, was es bedeutet, mit einem Beispiel. Die Texte stehen in `app/schemas.py` und landen auch als Kommentare im generierten Client. Die Datei dazu ist [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json). Im Ordner der React-App:

```powershell
npx @openapitools/openapi-generator-cli generate -i http://127.0.0.1:8000/openapi.json -g typescript-axios -o client-node
```

Node.js und Java. `axios` ist eine Abhängigkeit der App. Eine `Configuration` für alle drei Klassen:

```typescript
import { Configuration, GameHistoriesApi, ProfilesApi, UsersApi } from "./client-node";

const config = new Configuration({ basePath: "http://127.0.0.1:8000" });
const users = new UsersApi(config);
const profiles = new ProfilesApi(config);
const histories = new GameHistoriesApi(config);
```

## Wo welcher Aufruf hingehört

| Moment | Aufruf | Danach |
|---|---|---|
| Seite öffnet, Sitzplätze | `GET /users`, `GET /profiles` | Namen an die beiden Plätze X und O |
| Jemand ist neu | `POST /users`, dann `POST /profiles` | Der neue Name an einen Platz |
| Klick auf ein leeres Feld | kein Aufruf | Die Seite setzt das Zeichen selbst |
| Partie zu Ende | `POST /game-histories` | Die Antwort ist der gespeicherte Eintrag mit `id` |
| Lobby, Verlauf | `GET /game-histories` | Liste der fertigen Spiele |
| Ein Spiel nachschauen | `GET /game-histories/{history_id}` | Brett aus `game` zeichnen |

Ein Zug geht nicht an den Server. Beide Personen klicken im selben Fenster. Die Seite zeigt an, wer dran ist, und prüft nach jedem Klick auf eine Linie oder ein volles Brett.

## Spiel

### Sitzplätze

`GET /users` liefert die Konten. `GET /profiles` liefert den Namen, der am Platz steht. `user_id` im Profil ist `id` beim User. Beim Start:

| User | Name | Profil |
|---|---|---|
| 1 | Ada | Ada |
| 2 | Ben | Ben |
| 3 | Cleo | Cleo |
| 4 | Dan | Dan |

Die Seite merkt sich zwei Namen. Einer spielt X, einer spielt O. Sie müssen verschieden sein, sonst weist der Server den Verlauf ab.

Ein neuer Mensch: zuerst `POST /users` mit `{ "name": "Eve" }`. Die Antwort ist `{"id": 5, "name": "Eve"}`. Danach `POST /profiles` mit `{ "user_id": 5, "display_name": "Eve" }`. Ohne Profil gibt es den Menschen trotzdem. Das Profil ist nur der angezeigte Name. Ein zweites Profil für dieselbe Id ist **400**.

### Brett

Neun Felder, Zeile für Zeile. Das ist auch die Reihenfolge im Array `game`:

```
0 1 2
3 4 5
6 7 8
```

Ein Feld ist `""`, `"X"` oder `"O"`. Die ersten drei Einträge sind die erste Zeile. `player_a` ist der Mensch hinter X, `player_b` hinter O.

Linien, die gewinnen: drei Zeilen (`0 1 2`, `3 4 5`, `6 7 8`), drei Spalten (`0 3 6`, `1 4 7`, `2 5 8`) und zwei Diagonalen (`0 4 8`, `2 4 6`). Ein volles Brett ohne Linie ist ein Unentschieden.

### Verlauf speichern

Wenn die Partie zu Ende ist: `POST /game-histories`. Ada (X) hat gegen Cleo (O) auf der Diagonale 0, 4, 8 gewonnen:

```json
{
  "player_a": "Ada",
  "player_b": "Cleo",
  "game": ["X", "O", "O", "", "X", "", "", "", "X"],
  "winner": "Ada"
}
```

**201.** Die Antwort ist derselbe Eintrag mit der `id`, die der Server vergibt:

```json
{
  "id": "4",
  "player_a": "Ada",
  "player_b": "Cleo",
  "game": ["X", "O", "O", "", "X", "", "", "", "X"],
  "winner": "Ada"
}
```

`id` ist `"4"`, weil `"1"` bis `"3"` schon aus den Testdaten stammen. Ein Unentschieden schickt `"winner": "draw"`.

Die Seite schickt keine `id`. Wer sie trotzdem mitschickt, wird nicht abgewiesen, der Server ignoriert sie.

### Verlauf lesen

`GET /game-histories` liefert alle fertigen Spiele. Nach dem Start sind es drei:

```json
[
  {
    "id": "1",
    "player_a": "Ada",
    "player_b": "Cleo",
    "game": ["X", "O", "O", "", "X", "", "", "", "X"],
    "winner": "Ada"
  },
  {
    "id": "2",
    "player_a": "Dan",
    "player_b": "Ada",
    "game": ["X", "X", "O", "X", "O", "", "O", "", ""],
    "winner": "Ada"
  },
  {
    "id": "3",
    "player_a": "Ben",
    "player_b": "Dan",
    "game": ["X", "O", "X", "X", "O", "O", "O", "X", "X"],
    "winner": "draw"
  }
]
```

Siege von Ada sind die Einträge mit `"winner": "Ada"`. Es gibt keinen zweiten Aufruf dafür, die Seite zählt selbst.

### Wenn der Browser die Antwort blockt (CORS)

Die App meldet `Network Error`, in der Browser-Konsole (F12) steht `blocked by CORS policy`. `/docs` und `curl` funktionieren trotzdem. Dann kennt der Server die Adresse deiner App nicht. Trag sie in `main.py` bei `allow_origins` ein, zum Beispiel `"http://localhost:5174"`, wenn Vite den Port 5174 nimmt. Schema, Host und Port müssen genau stimmen, ohne Schrägstrich am Ende. `localhost` und `127.0.0.1` zählen als verschiedene Adressen. Die ausführliche Tabelle steht in `README.md` im Abschnitt CORS.

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

### `POST /game-histories`

Fertiges Spiel speichern. `histories.createHistoryGameHistoriesPost({ player_a, player_b, game, winner })`.

Body `GameHistoryCreate`:

| Feld | Bedeutung |
|---|---|
| `player_a` | Name der Person mit X |
| `player_b` | Name der Person mit O |
| `game` | Neun Strings, Index 0–8. `""`, `"X"` oder `"O"` |
| `winner` | Name von `player_a` oder `player_b`, oder `"draw"` |

**201.** `GameHistoryResponse`: dieselben Felder plus `id` (Text).

**400.** Die Meldung steht in `detail`:

| `detail` | Wann |
|---|---|
| `Player name is empty` | `player_a` oder `player_b` leer oder nur Leerzeichen |
| `Players must differ` | beide Namen gleich |
| `Game must have nine cells` | `game` hat nicht genau neun Einträge |
| `Cell must be empty, X, or O` | ein Feld ist etwas anderes |
| `Winner must be a player or draw` | `winner` ist weder `player_a` noch `player_b` noch `"draw"` |

**422.** Ein Feld fehlt oder hat den falschen Typ. Das prüft FastAPI vor dem Service.

### `GET /game-histories`

Verlauf, Lobby. `histories.listHistoriesGameHistoriesGet()`.

**200.** Liste von `GameHistoryResponse`.

### `GET /game-histories/{history_id}`

Ein fertiges Spiel nachschauen. `histories.getHistoryGameHistoriesHistoryIdGet(historyId)`.

**200.** `GameHistoryResponse`:

| Feld | Bedeutung |
|---|---|
| `id` | Eintrag, als Text |
| `player_a` | Name der Person mit X |
| `player_b` | Name der Person mit O |
| `game` | Neun Strings, Index 0–8. `""`, `"X"` oder `"O"` |
| `winner` | Name des Siegers oder `"draw"` |

**404.** `Game history not found`.
