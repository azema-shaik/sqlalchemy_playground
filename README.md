# SQLAlchemy Log‑Ingestion Playground

This mini‑repo is a **learning playground** for SQLAlchemy 2.0.  It shows how to

- generate synthetic infrastructure logs,
- model a small relational schema, and then
- ingest those logs into **both synchronous and asynchronous** SQLite databases – all with modern Python 3.11 idioms.

> Use it as a reference or rip it apart for experiments; the goal is to get a feel for SQLAlchemy’s Core & ORM APIs while keeping the code footprint small.

---

## Project layout

| Path                       | Purpose                                                                                                                                                                                                                          |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `log_genrator.py`          | CLI script that fabricates coloured JSONL log files and (optionally) a matching *employees.json* roster.  It supports rotation, seeded determinism, and a quick **cleanse** flag to wipe old runs. fileciteturn1file6L67-L75 |
| `config.json`              | Single source of truth for connection URLs and filesystem roots. fileciteturn1file3L2-L6                                                                                                                                     |
| `models.py`                | Declarative ORM models (`Department ↔ Employee ↔ Log`) plus tiny mix‑ins for `__repr__` and JSON serialisation. fileciteturn1file4L18-L24                                                                                    |
| `engine.py`                | Loads `config.json`, spins up **both** a sync and async engine and keeps a ready‑to‑use `Session`.                                                                                                                               |
| `creating_tables.py`       | *Synchronous* pipeline: create tables, bulk‑insert reference data, then stream logs from disk into the DB.  Timestamps are normalised to UTC as they are ingested. fileciteturn1file11L40-L42                                |
| `creating_tables_async.py` | Same pipeline but using `AsyncSession`/`async_sessionmaker` and `create_async_engine`. fileciteturn1file1L58-L63                                                                                                             |

---

## Quick‑start

> **Prerequisites** : Python ≥ 3.11 and `pip`.  SQLite is bundled; no external database is required.

```bash
# 1 – Clone and enter the repo
$ git clone <your-fork-url> sqlachemy-playground
$ cd sqlalchemy-playground

# 2 – Install runtime deps (SQLAlchemy, aiosqlite, faker, etc.)
$ pip install -r requirements.txt

# 3 – Generate 10k log lines split into 2k‑line chunks & persist employees & also cleanses previous files
$ python log_genrator.py -t 10000 -p 2000 -e -c

# 4a – Load data the **sync** way (blocks the event‑loop but simplest)
$ python creating_tables.py

# 4b – —or— load data **async** (non‑blocking path)
$ python creating_tables_async.py
```

Both scripts leave you with `logs_sync.db` **and/or** `logs_async.db` (SQLite) ready to explore via your favourite viewer.

---

## Database schema

```text
Department (id  PK,  name)
    └───< Employee (emp_id  PK,  first_name, last_name, gender, department_id FK)
                └───< Log (log_id  PK, employee_id FK, dt, level, ip, msg)
```

- **Department ↔ Employee**: one‑to‑many, bidirectional via `relationship(back_populates=...)`. fileciteturn1file4L22-L36
- **Employee ↔ Log**: one‑to‑many with cascade only at insert for learning simplicity. fileciteturn1file4L41-L48
- `dt` timestamps are parsed *with zone‑offset* and converted to UTC on insert.

---

## Configuration

`config.json` lets you point the pipeline at any RDBMS supported by SQLAlchemy. Just swap out the URLs (e.g. `postgresql+psycopg://user:pass@localhost/logs`).  Both engines are wired from the same file so you only edit in one place.

---

## Log generator tips

- **Determinism** : pass `-r` to disable new randomness and replay the same data via `--random-seed`.
- **Rotation** : `-p/--per-file` sets the JSONL chunk size (defaults to 1000).
- **Purge** : `-c/--cleanse` wipes the entire *logs/* directory before running.

---

## Extending the playground

- Point `connection_url_*` at Postgres or MariaDB to test different dialects.
- Swap `aiosqlite` for `asyncpg` to learn about async drivers.
- Add `pytest` fixtures around the generator and make assertions on row counts.
- Experiment with `selectinload()` / `joinedload()` to benchmark eager loading.

---

## Licence

MIT – have fun and learn!

