# Server-Starter

HTTP-Anwendung mit einer Nachricht. Keine Datenbank. Der Speicher ist ein Dict und startet mit `{"id": 1, "text": "hello"}`.

`main.py` verbindet drei Schichten. Jede kennt nur die darunter.

| Schicht | Name | Datei |
|---|---|---|
| Daten | `MessageRepository` | `message_repository.py` |
| Logik | `MessageService` | `message_service.py` |
| Präsentation | `build_router` | `message_router.py` |

`Message` in `message.py` ist das Objekt zwischen den Schichten: `id` und `text`.

Daten: `list_all`, `get`, `add`, `replace`, `remove`.

Logik: `list_messages`, `get_message`, `create_message`, `update_message`, `delete_message`.

Routen:

- `GET /messages`
- `GET /messages/{message_id}`
- `POST /messages` mit `{"text": "..."}`
- `PUT /messages/{message_id}` mit `{"text": "..."}`
- `DELETE /messages/{message_id}`

## Requirements

Python 3.14.

Direkte Abhängigkeiten, Versionen aus der `.venv` dieses Projekts:

- `fastapi` 0.142.2
- `uvicorn` 0.54.0

Die Namen stehen in `requirements.txt`.

## Abhängigkeiten

FastAPI ist die HTTP-Anwendung. In `main.py` steht `app = FastAPI()`. Die Routen stehen in `message_router.py`. Eine Route ist eine URL plus eine Funktion. `@router.get("/messages")` liefert die Liste.

Die Funktion gibt ein Modell zurück. FastAPI macht daraus JSON. Die erste Nachricht ist `{"id": 1, "text": "hello"}`.

FastAPI schreibt die OpenAPI-Beschreibung selbst: Pfad, Methode, JSON. Das ist keine zweite Datei. Die Seite ist `/docs`. Das Schema liegt unter `/openapi.json`. Eine neue Route erscheint dort, sobald der Server sie geladen hat.

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

Liste: [http://127.0.0.1:8000/messages](http://127.0.0.1:8000/messages)

Beschreibung: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Stop

Im selben Terminal **Strg+C**. Die Eingabezeile kommt zurück. Die Adressen antworten nicht mehr.

## Lizenz

MIT. Siehe [LICENSE.md](LICENSE.md).
