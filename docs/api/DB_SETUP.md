# Database Setup — PostgreSQL + PostGIS

## Prerequisites

- **Docker** and **Docker Compose** installed ([Get Docker](https://docs.docker.com/get-docker/))

## 1. Start the database

```bash
# From the repo root
cd docker
docker compose up -d
```

This pulls `postgis/postgis:16-3.4` (Postgres 16 with PostGIS 3.4), creates a persistent volume (`pgdata`), and exposes Postgres on port **5432**.

### Verify the container is healthy

```bash
docker compose ps
```

The `sevasangam_db` container should show **healthy** status within ~30 seconds.

## 2. Confirm PostGIS is enabled

Connect to the database and check:

```bash
docker compose exec db psql -U sevasangam -d sevasangam
```

Inside the `psql` shell:

```sql
-- PostGIS should already be available in the postgis/postgis image.
-- Create the extension (idempotent):
CREATE EXTENSION IF NOT EXISTS postgis;

-- Verify:
SELECT PostGIS_Full_Version();
```

You should see output like:

```
POSTGIS="3.4.x ..." PGSQL="160" ...
```

Type `\q` to exit.

## 3. Environment variables

Copy the backend env template and adjust if needed:

```bash
cp backend/.env.example backend/.env
```

Default values work out of the box with the Docker Compose service:

| Variable | Default | Notes |
| --- | --- | --- |
| `POSTGRES_USER` | `sevasangam` | DB superuser |
| `POSTGRES_PASSWORD` | `sevasangam_dev` | **Change in production** |
| `POSTGRES_DB` | `sevasangam` | Database name |
| `POSTGRES_HOST` | `localhost` | Use `db` if the backend also runs inside Docker |
| `POSTGRES_PORT` | `5432` | Host-mapped port |

## 4. Stop / reset

```bash
# Stop (keeps data)
docker compose down

# Stop AND delete the volume (full reset)
docker compose down -v
```

## 5. Connecting from the backend

The backend uses SQLAlchemy with `asyncpg`. The connection string is built from the env vars above:

```
postgresql+asyncpg://sevasangam:sevasangam_dev@localhost:5432/sevasangam
```

> **Note:** If you run the backend inside the same Docker network, replace `localhost` with the service name `db`.
