# db-boilerplate

Docker boilerplate with **FastAPI**, **PostgreSQL**, and **MongoDB**, ready to run with a single command. Use this as the starting point for building your own endpoints.

---

## Prerequisites

You need these installed on your machine:

- [Docker](https://docs.docker.com/get-docker/) (Docker Desktop on Windows/Mac, Docker Engine on Linux)
- [Docker Compose](https://docs.docker.com/compose/install/) (included with Docker Desktop)
- [Git](https://git-scm.com/downloads)

Verify they are installed:

```bash
docker --version
docker compose version
git --version
```

---

## 1. Clone the repository

```bash
git clone https://github.com/Alex23013/db-boilerplate.git
cd db-boilerplate
```

---

## 2. Start the containers

From the project root, run:

```bash
docker compose up --build
```

The first run will take a few minutes (it pulls the Postgres, Mongo, and Python images and installs the Python dependencies). When it's ready you should see logs like:

```
fastapi_app  | Uvicorn running on http://0.0.0.0:8000
postgres_db  | database system is ready to accept connections
mongo_db     | Waiting for connections
```

Leave that terminal running. Open a **new terminal** for the verification steps below.

> To run the containers in the background instead, use `docker compose up --build -d`.

---

## 3. Verify everything is running

### Check the containers are up

```bash
docker compose ps
```

You should see three services with status `running` (or `healthy`): `api`, `postgres`, `mongo`.

### Check FastAPI

Open in your browser: <http://localhost:8000>

You should see:

```json
{"status": "ok"}
```

FastAPI also auto-generates interactive API docs. Open: <http://localhost:8000/docs>

### Check PostgreSQL

Visit: <http://localhost:8000/health/postgres>

You should see a response with the Postgres version, e.g.:

```json
{"version": "PostgreSQL 16.x ..."}
```

If you want to connect to Postgres directly with `psql`:

```bash
docker compose exec postgres psql -U postgres -d appdb
```

Default credentials (dev only): user `postgres`, password `postgres`, database `appdb`, port `5432`.

### Check MongoDB

Visit: <http://localhost:8000/health/mongo>

You should see:

```json
{"mongo_version": "7.x.x"}
```

To open a Mongo shell directly:

```bash
docker compose exec mongo mongosh -u mongo -p mongo
```

Default credentials (dev only): user `mongo`, password `mongo`, port `27017`.

---

## 4. Stopping the containers

In the terminal running `docker compose up`, press `Ctrl+C`.

To remove the containers (data in the named volumes is preserved):

```bash
docker compose down
```

To also wipe the database data:

```bash
docker compose down -v
```

---

## Project structure

```
.
├── Dockerfile              # Builds the FastAPI app image
├── docker-compose.yml      # Orchestrates api + postgres + mongo
├── requirements.txt        # Python dependencies
├── app/
│   └── main.py             # FastAPI app — edit this to add endpoints
└── README.md
```

The `app/` folder is mounted into the container, so any edits you make to `app/main.py` will hot-reload — no need to rebuild the image while developing.

---

## Troubleshooting

- **"Port already in use" / address conflict**: Another process is using port `8000`, `5432`, or `27017`. Stop the conflicting service, or change the host-side port in `docker-compose.yml` (e.g. `"8001:8000"`).
- **`docker: command not found`**: Docker isn't installed or isn't on your `PATH`. Reinstall Docker Desktop and restart your terminal.
- **Changes to `requirements.txt` aren't picked up**: Rebuild the image with `docker compose up --build`.
- **Want a clean slate**: `docker compose down -v` removes containers and database volumes so the next `up` starts fresh.
