# Server-Starter

Backend für Tic-Tac-Toe. Keine Datenbank. Der Speicher ist ein Dict. Zwei Personen, ein Browser. Der Client schickt beide User-Ids, wenn ein Spiel startet.

Die Regeln stehen in `aufgabe.md`. Die gespeicherten Zeilen stehen in `app/domain/models.py`. Die JSON-Formen stehen in `app/schemas.py`.

`main.py` verbindet drei Schichten. Jede kennt nur die darunter. Pro Ressource ein Paket unter `app/`.

| Schicht | Name | Datei |
|---|---|---|
| Daten | `UserRepository` und die anderen Repositories | `app/*/repository.py` |
| Logik | `UserService` und die anderen Services | `app/*/service.py` |
| Präsentation | `build_router` | `app/*/router.py` |

`User` in `app/domain/models.py` ist das Objekt zwischen den Schichten: `id` und `name`. `Profile`, `Game` und `Score` sind die weiteren Zeilen.

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
| `POST /games` | **201** `GameResponse`. Leeres Brett, `next` ist `"X"`, `status` ist `in_progress`. Gleicher User oder unbekannter User: **400** bzw. **404**. |
| `GET /games` | Liste von `GameResponse`. |
| `GET /games/{game_id}` | Ein Spiel. Unbekannt: **404**. |
| `POST /games/{game_id}/moves` | `GameResponse`. Der Zug ist nur `cell`. Das Zeichen kommt aus `next`. Beendet, Feld außerhalb 0–8 oder belegt: **400**. Am Ende ist `next` `null`, und es entstehen zwei Score-Zeilen. |
| `GET /scores` | Liste von `ScoreHistoryResponse`. Gewonnen, verloren und unentschieden stehen in `result`. |

## Testdaten

Beim Start lädt `main.py` `load_fixtures` aus `app/fixtures.py` in dieselben Dicts. Keine Datei, keine Datenbank. Ein Neustart oder `--reload` wirft nachträglich angelegte Zeilen weg und lädt diese Ids wieder. `played_at` ist die Uhrzeit dieses Starts.

| Id | Inhalt |
|---|---|
| User 1–4 | Ada, Ben, Cleo, Dan. Je ein Profil, `display_name` gleich dem Namen. |
| Spiel 1 | Ada (X) gegen Ben (O). Laufend, Züge 0, 1, 4. `next` ist `"O"`. |
| Spiel 2 | Cleo (X) gegen Dan (O). Leeres Brett, `in_progress`. |
| Spiel 3 | Ada (X) gegen Cleo (O). `x_wins` auf 0, 4 und 8. Zwei Score-Zeilen, `win` und `loss`. |
| Spiel 4 | Dan (X) gegen Ada (O). `o_wins`. Zwei Score-Zeilen. |
| Spiel 5 | Ben (X) gegen Dan (O). Volles Brett, `draw`. Zwei Score-Zeilen. |

`GET /users`, `GET /profiles`, `GET /games`, `GET /games/1` und `GET /scores` liefern diese Menge. Ein `POST` hängt dahinter an. Der nächste User ist die Id 5.

## Requirements

Python 3.14.

Direkte Abhängigkeiten, Versionen aus der `.venv` dieses Projekts:

- `fastapi` 0.142.2
- `uvicorn` 0.54.0

Die Namen stehen in `requirements.txt`.

## Abhängigkeiten

FastAPI ist die HTTP-Anwendung. In `main.py` steht `app = FastAPI()`. Die Routen stehen in `app/*/router.py`. `@router.post` nimmt eine Form aus `app/schemas.py` und gibt eine zurück. FastAPI macht daraus JSON.

FastAPI schreibt die OpenAPI-Beschreibung selbst: Pfad, Methode, JSON. Das ist keine zweite Datei. Die Seite ist `/docs`. Das Schema liegt unter `/openapi.json`.

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

Der Prozess läuft, wenn das Terminal offen bleibt und `Uvicorn running on http://127.0.0.1:8000` zeigt. Der Browser unter `http://127.0.0.1:5173` und `http://localhost:5173` darf die API aufrufen.

## OpenAPI

FastAPI schreibt die Beschreibung beim Start. Im Projektordner liegt keine OpenAPI-Datei.

Die Seite zum Lesen und Ausprobieren ist [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). Dort stehen Users, Profiles, Games und Scores. Die Adresse `/` hat keine Route.

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
