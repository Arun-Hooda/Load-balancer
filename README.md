# Load-Balanced Multi-Instance App

A small Flask app running as **3 identical Docker containers** behind an **Nginx load balancer**.
Each refresh of the page is answered by a different container, which shows horizontal scaling.

## Architecture

```
            +--> app1 (Server 1)
Client --> Nginx (port 8080) --> app2 (Server 2)
 (browser)  (load balancer)  +--> app3 (Server 3)
```

- **Client**: your browser or curl.
- **Nginx**: receives every request and forwards it to the next server in turn (round-robin).
- **app1/2/3**: the same Flask app, each started with a different `SERVER_NAME`.
- Everything is defined in `docker-compose.yml` and runs locally.

## How to run

Requirements: Docker Desktop (or Docker + Docker Compose).

```bash
docker compose up --build
```

Open http://localhost:8080 and refresh. The server name cycles Server 1 -> 2 -> 3.

Or from a terminal:

```bash
for i in 1 2 3 4 5 6; do curl -s localhost:8080/api/whoami; echo; done
```

Stop with `Ctrl+C`, then `docker compose down`.

Failure demo: `docker compose stop app2`, then refresh. The site keeps working
(nginx routes around the dead server).

## Run the tests

```bash
pip install -r requirements-dev.txt
pytest -v
```

## CI/CD

GitHub Actions (`.github/workflows/ci.yml`) runs on every push and pull request:
1. `test`: installs dependencies and runs pytest (5 tests).
2. `docker-build`: builds the containers (only if tests pass).

Branch protection on `main` requires the `test` check to pass before merging,
so failing code cannot be merged.

## Endpoints

| Path | Returns |
|---|---|
| `/` | HTML page showing which server answered |
| `/api/whoami` | JSON `{"server": "Server N"}` |
| `/health` | JSON `{"status": "ok"}` |
