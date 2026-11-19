# Server-Starter

Backend für Tic-Tac-Toe. Keine Datenbank. Der Speicher ist ein Dict. Zwei Personen, ein Browser. Die React-App spielt das Spiel selbst. Der Server speichert nur den Verlauf: ein fertiges Spiel pro Eintrag.

Die Regeln stehen in `aufgabe.md`. Der Weg für ein React-Frontend steht in `frontend.md`. Die gespeicherten Zeilen stehen in `app/domain/models.py`. Die JSON-Formen stehen in `app/schemas.py`.

`main.py` verbindet drei Schichten. Jede kennt nur die darunter. Pro Ressource ein Paket unter `app/`.

| Schicht | Name | Datei |
|---|---|---|
| Daten | `UserRepository` und die anderen Repositories | `app/*/repository.py` |
| Logik | `UserService` und die anderen Services | `app/*/service.py` |
| Präsentation | `build_router` | `app/*/router.py` |

`User` in `app/domain/models.py` ist das Objekt zwischen den Schichten: `id` und `name`. `Profile` und `GameHistory` sind die weiteren Zeilen.

`GET /users` beginnt mit Ada. Das ist `UserResponse`:

```json
{"id": 1, "name": "Ada"}
```

Ein neues `POST /users` hängt an und bekommt die nächste Id. Der Body ist `UserCreate`. Ein leerer Name ist **400**.

| Aufruf | Antwort |
|---|---|
| `POST /users` | **201** `UserResponse`. Leerer Name: **400**. |
| `GET /users` | Liste von `UserResponse`. |
| `POST /profiles` | **201** `ProfileResponse`. Unbekannter User: **404**. Zweites Profil: **400**. |
| `GET /profiles` | Liste von `ProfileResponse`. |
| `POST /game-histories` | **201** `GameHistoryResponse`. Der Body ist `GameHistoryCreate`, ohne `id`. Ungültiger Eintrag: **400**. |
| `GET /game-histories` | Liste von `GameHistoryResponse`. |
| `GET /game-histories/{history_id}` | Ein Eintrag. Unbekannt: **404**. |

Ein Eintrag ist ein fertiges Spiel:

```json
{
  "id": "1",
  "player_a": "Ada",
  "player_b": "Cleo",
  "game": ["X", "O", "O", "", "X", "", "", "", "X"],
  "winner": "Ada"
}
```

| Feld | Bedeutung |
|---|---|
| `id` | Text. Vergibt der Server: `"1"`, `"2"`, … Der Client schickt sie nicht. |
| `player_a` | Name der Person mit X |
| `player_b` | Name der Person mit O |
| `game` | Neun Strings, Zeile für Zeile. Die ersten drei sind die erste Zeile. Ein Feld ist `""`, `"X"` oder `"O"`. |
| `winner` | Name von `player_a` oder `player_b`, oder `"draw"` |

**400**, wenn ein Name leer ist, beide Namen gleich sind, `game` nicht neun Felder hat, ein Feld ungültig ist oder `winner` weder ein Spieler noch `"draw"` ist. Die Meldung steht in `detail`.

## Testdaten

Beim Start lädt `main.py` `load_fixtures` aus `app/fixtures.py` in dieselben Dicts. Keine Datei, keine Datenbank. Ein Neustart oder `--reload` wirft nachträglich angelegte Zeilen weg und lädt diese Ids wieder.

| Id | Inhalt |
|---|---|
| User 1–4 | Ada, Ben, Cleo, Dan. Je ein Profil, `display_name` gleich dem Namen. |
| Verlauf `"1"` | Ada (X) gegen Cleo (O). X gewinnt auf 0, 4 und 8. `winner` ist `"Ada"`. |
| Verlauf `"2"` | Dan (X) gegen Ada (O). O gewinnt auf 2, 4 und 6. `winner` ist `"Ada"`. |
| Verlauf `"3"` | Ben (X) gegen Dan (O). Volles Brett, keine Linie. `winner` ist `"draw"`. |

`GET /users`, `GET /profiles`, `GET /game-histories` und `GET /game-histories/1` liefern diese Menge. Ein `POST` hängt dahinter an. Der nächste User ist die Id 5, der nächste Verlauf die Id `"4"`.

## Computer-Gegner

Ein Agent mit einem Sprachmodell (Ollama, Pydantic AI) wählt den nächsten Zug. Die App schickt das Brett, der Server antwortet mit dem Feld. Es wird nichts gespeichert.

| Aufruf | Antwort |
|---|---|
| `POST /computer-moves` | **200** `ComputerMoveResponse` mit `position` (0 bis 8). Body `ComputerMoveRequest` (nicht `Create`: der Server legt nichts an, er beantwortet eine Frage): `game` (neun Felder) und `mark` (`"X"` oder `"O"`, das Zeichen des Computers). Die App schickt immer ein Brett mit neun Feldern. Der Server prüft das Brett nicht und hat keine eigenen Fehlercodes. |

```json
{"game": ["X", "O", "", "", "X", "", "", "", "O"], "mark": "O"}
```

Die Route ist `async`, weil der Agent auf das Sprachmodell wartet. Der Server bleibt in dieser Zeit frei.

Die Dateien stehen in `app/computer_moves/`:

| Datei | Aufgabe |
|---|---|
| `tools.py` | Die Funktionsaufrufe (Function Calls) des Agenten. **Hier erweiterst du.** |
| `agent.py` | `SYSTEM_PROMPT` (wer der Agent ist) und `create_game_agent()` (Modell aus der Umgebung, Standard `llama3.2`). |
| `service.py` | Startet den Agenten (höchstens 6 Modellaufrufe pro Zug) und gibt das Feld zurück, das der Funktionsaufruf gesetzt hat. Schreibt jeden Funktionsaufruf ins Terminal. |
| `router.py` | Die Route `POST /computer-moves`. |

Der Zug kommt vom Funktionsaufruf `place_computer_mark`, nie aus dem Text des Modells. Ist das Feld belegt, meldet die Funktion den Fehler und die freien Felder. Das Modell versucht es dann noch einmal.

Das Terminal zeigt jeden Funktionsaufruf, auch einen, den du in `tools.py` ergänzt. `main.py` schaltet das Logging einmal ein. Ein Zug sieht so aus:

```text
INFO app.computer_moves: choose_move mark=O
INFO app.computer_moves: tool call place_computer_mark {'position': 2}
INFO app.computer_moves: tool result place_computer_mark: Placed O at position 2.
INFO app.computer_moves: choose_move position=2
```

### Ein Funktionsaufruf, der gut gebaut ist

Das Modell sieht nie den Python-Code. Es bekommt ein Schema aus drei Dingen: Funktionsname, Parameter und Docstring. Daran entscheidet es, ob und womit es die Funktion aufruft.

- **Name:** Verb und Objekt, was die Funktion tut. `place_computer_mark`, nicht `do_it` oder `move2`.
- **Parameter:** wenige, mit klarem Typ und Namen. `position: int`.
- **Docstring:** wofür die Funktion da ist und wann man sie nutzt. Nicht, wie sie es macht. Jeder Parameter mit Bedeutung und Wertebereich.

```python
def place_computer_mark(ctx: RunContext[GameContext], position: int) -> str:
    """Place the computer's mark on one free cell of the board. Use this to make the computer's move.

    position: the cell, a whole number from 0 to 8. 0 to 2 is the top row, 3 to 5 the middle row, 6 to 8 the bottom row.
    """
```

### Einen weiteren Funktionsaufruf ergänzen

1. Eine Funktion in `app/computer_moves/tools.py` schreiben, mit `ctx: RunContext[GameContext]` als erstem Parameter. `ctx.deps` ist der `GameContext` dieses Zugs: `board`, `mark` und `move`.
2. Sie in die Liste `TOOLS` am Ende der Datei eintragen.

Eine normale `def`-Funktion reicht. `async def` brauchst du nur, wenn die Funktion selbst auf etwas Langsames wartet (HTTP-Aufruf, Datenbank). Die Route und `choose_move` sind `async`, weil sie auf das Sprachmodell warten. `place_computer_mark` wartet auf nichts.

Sonst ändert sich nichts. Der Aufruf erscheint von selbst im Terminal. Ideen: `list_free_positions`, `find_winning_position`, `find_blocking_position`. Das sind Hilfen, die nur lesen. Das Modell ruft sie vor `place_computer_mark` auf. Probiere, was ein anderer Name oder ein anderer Docstring ändert.

### Modell

Ollama muss laufen und das Modell geladen sein (`ollama pull llama3.2`). Ohne Datei `.env` nimmt der Server `llama3.2`. Ein anderes Modell: `.env.example` nach `.env` kopieren und `MODEL_NAME` ändern. `main.py` lädt die Datei einmal beim Start mit `load_dotenv()`, danach liest `create_game_agent()` die Werte aus der Umgebung. Echte Umgebungsvariablen haben Vorrang vor der Datei. Kleine Modelle spielen nicht gut Tic-Tac-Toe: sie wählen belegte Felder oder übersehen einen Gewinnzug. Genau deshalb prüft die Funktion jeden Zug.

## Requirements

Python 3.14.

Direkte Abhängigkeiten, Versionen aus der `.venv` dieses Projekts:

- `fastapi` 0.142.2
- `uvicorn` 0.54.0
- `pydantic-ai-slim[openai]` 2.69.0
- `python-dotenv` 1.2.4

Die Namen stehen in `requirements.txt`.

## Abhängigkeiten

FastAPI ist die HTTP-Anwendung. In `main.py` steht `app = FastAPI()`. Die Routen stehen in `app/*/router.py`. `@router.post` nimmt eine Form aus `app/schemas.py` und gibt eine zurück. FastAPI macht daraus JSON.

FastAPI schreibt die OpenAPI-Beschreibung selbst: Pfad, Methode, JSON. Das ist keine zweite Datei. Die Seite ist `/docs`. Das Schema liegt unter `/openapi.json`.

Die Texte dazu stehen im Code, nicht in einer eigenen Datei. In `app/schemas.py` hat jedes Feld eine Beschreibung und ein Beispiel:

```python
from typing import Annotated
from pydantic import Field

@dataclass
class UserCreate:
    """Body für einen neuen Account. Die `id` vergibt der Server."""

    name: Annotated[str, Field(description="Name des neuen Accounts. Pflicht.", examples=["Ada"])]
```

- Das Docstring der Klasse wird zur Beschreibung des ganzen Schemas.
- `Field(description=...)` beschreibt ein Feld. `examples=[...]` ist das Beispiel, das `/docs` im Body vorbelegt.
- `Path(description=...)` beschreibt einen Pfad-Parameter, hier `history_id` in `app/game_histories/router.py`.
- Der Generator übernimmt die Texte als Kommentare in `client-node`.
- Ein neues Feld braucht immer eine Beschreibung und ein Beispiel.

Uvicorn ist der Prozess, der Verbindungen annimmt. FastAPI öffnet keinen Port. `python main.py` legt nur das App-Objekt an und beendet sich. Uvicorn lädt `app` aus `main.py` und reicht jede Anfrage dorthin.

`uvicorn main:app --reload`: `main` ist die Datei `main.py`, `app` ist die Variable `app = FastAPI()`. `--reload` startet neu, wenn eine Datei gespeichert wird. Der Server hört auf `http://127.0.0.1:8000`.

## Setup

Die Pakete liegen in einer `.venv` in diesem Ordner, nicht im globalen Python. Einmalig:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Nach `Activate.ps1` steht `(.venv)` vor der Eingabezeile. Ohne diese Installation ist der Befehl `uvicorn` unbekannt.

## Start

```powershell
uvicorn main:app --reload
```

Der Prozess läuft, wenn das Terminal offen bleibt und `Uvicorn running on http://127.0.0.1:8000` zeigt. Der Browser unter `http://127.0.0.1:5173` und `http://localhost:5173` darf die API aufrufen. Läuft deine App unter einer anderen Adresse, lies den Abschnitt CORS.

## CORS

Der Browser lässt eine Seite nur dann die API einer anderen Adresse aufrufen, wenn der Server das erlaubt. Das ist CORS. Eine Adresse ist Schema, Host und Port zusammen. `http://localhost:5173` und `http://127.0.0.1:5173` sind zwei verschiedene Adressen. Die Erlaubnis steht in `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Auf deinem Rechner musst du die Liste vielleicht ändern:

| Situation | Was tun |
|---|---|
| Vite meldet `Local: http://localhost:5174`, weil 5173 belegt ist | `"http://localhost:5174"` in die Liste |
| Du öffnest die App über `http://127.0.0.1:...` statt `localhost` | die passende Adresse eintragen |
| Die React-App läuft auf einem anderen Port, zum Beispiel 3000 | `"http://localhost:3000"` eintragen |
| Du rufst die App von einem anderen Rechner auf | `"http://<Adresse-des-Rechners>:5173"` eintragen |

Kein Schrägstrich am Ende, kein Pfad: `"http://localhost:5174"`, nicht `"http://localhost:5174/"`. Nach dem Speichern lädt `--reload` den Server neu.

So erkennst du ein CORS-Problem:
- In der Browser-Konsole (F12) steht `blocked by CORS policy: No 'Access-Control-Allow-Origin' header`.
- Die React-App meldet `Network Error` und zeigt keine Daten. Im Server-Terminal steht entweder `OPTIONS ... 400 Bad Request` (die Vorab-Anfrage des Browsers bei `POST`) oder ein `200 OK`, das die App trotzdem nicht bekommt.
- `/docs` und `curl` funktionieren trotzdem. Beide laufen nicht im Browser unter einer fremden Adresse.

Das ist kein Fehler in der API und auch keiner im Client. Ein `"*"` in `allow_origins` erlaubt jede Adresse. Das geht lokal zum Üben, in einer echten Anwendung nicht.

Die Basis-Adresse des Servers steht im Client: `new Configuration({ basePath: "http://127.0.0.1:8000" })`. Läuft uvicorn auf einem anderen Port (`--port 8001`), ändere sie dort.

## OpenAPI

FastAPI schreibt die Beschreibung beim Start. Im Projektordner liegt keine OpenAPI-Datei.

Die Seite zum Lesen und Ausprobieren ist [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). Dort stehen Users, Profiles und Game-Histories. Die Adresse `/` hat keine Route.

Die Datei selbst ist [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json). Das Format ist OpenAPI 3.1. Im Browser öffnen oder speichern, während der Server läuft:

```powershell
curl.exe -o openapi.json http://127.0.0.1:8000/openapi.json
```

Daraus baut ein Generator einen Client. Die andere App ruft damit die API auf. Der Client gehört in diese App, nicht in dieses Repository. Der Generator braucht Node.js und Java.

Python:

```powershell
npx @openapitools/openapi-generator-cli generate -i http://127.0.0.1:8000/openapi.json -g python -o client-python
```

```python
import openapi_client
from openapi_client.models.user_create import UserCreate

configuration = openapi_client.Configuration(host="http://127.0.0.1:8000")

with openapi_client.ApiClient(configuration) as api_client:
    api = openapi_client.UsersApi(api_client)
    user = api.create_user_users_post(UserCreate(name="Ada"))
    print(user.id, user.name)
```

Node, als TypeScript:

```powershell
npx @openapitools/openapi-generator-cli generate -i http://127.0.0.1:8000/openapi.json -g typescript-axios -o client-node
```

```typescript
import { Configuration, UsersApi } from "./client-node";

const api = new UsersApi(
  new Configuration({ basePath: "http://127.0.0.1:8000" })
);
const response = await api.createUserUsersPost({ name: "Ada" });
console.log(response.data);
```

Der Methodenname kommt aus der `operationId` im Schema. Hier heißt sie `create_user_users_post`.

## Stop

Im selben Terminal **Strg+C**. Die Eingabezeile kommt zurück. Die Adresse antwortet nicht mehr.

## Lizenz

MIT. Siehe [LICENSE.md](LICENSE.md).
