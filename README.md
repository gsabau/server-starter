# Server-Starter

Backend für Tic-Tac-Toe. Keine Datenbank. Der Speicher ist ein Dict. Zwei Personen, ein Browser. Der Client schickt beide User-Ids, wenn ein Spiel startet.

Dieses Beispiel legt nur einen User an. Die übrigen Aufrufe stehen in `aufgabe.md`. Die gespeicherte Zeile steht in `domain/models.py`. Die DTOs stehen in `dtos/dtos.py`.

`main.py` verbindet drei Schichten. Jede kennt nur die darunter.

| Schicht | Name | Datei |
|---|---|---|
| Daten | `UserRepository` | `user_repository.py` |
| Logik | `UserService` | `user_service.py` |
| Präsentation | `build_router` | `user_router.py` |

`User` in `domain/models.py` ist das Objekt zwischen den Schichten: `id` und `name`.

`POST /users` mit `{"name": "Ada"}` antwortet **201**:

```json
{"id": 1, "name": "Ada"}
```

Der Body ist `UserCreate`. Die Antwort ist `UserResponse`. Ein leerer Name ist **400**.

## Requirements

Python 3.14.

Direkte Abhängigkeiten, Versionen aus der `.venv` dieses Projekts:

- `fastapi` 0.142.2
- `uvicorn` 0.54.0

Die Namen stehen in `requirements.txt`.

## Abhängigkeiten

FastAPI ist die HTTP-Anwendung. In `main.py` steht `app = FastAPI()`. Die Route steht in `user_router.py`. `@router.post("/users")` nimmt `UserCreate` und gibt `UserResponse` zurück. FastAPI macht daraus JSON.

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

Der Prozess läuft, wenn das Terminal offen bleibt und `Uvicorn running on http://127.0.0.1:8000` zeigt.

## OpenAPI

FastAPI schreibt die Beschreibung beim Start. Im Projektordner liegt keine OpenAPI-Datei.

Die Seite zum Lesen und Ausprobieren ist [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). Dort steht `POST /users`. Die Adresse `/` hat keine Route.

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
