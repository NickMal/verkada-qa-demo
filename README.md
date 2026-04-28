# Verkada QA Demo

A 2-day QA interview demo combining a Playwright UI suite that exercises the real Verkada Command web UI (`command.verkada.com`) against a trial account, and a small FastAPI **mock** server that simulates a slice of the public Verkada API for hermetic API-level tests. The UI tests drive a headed Chromium browser through real login + TOTP and a handful of in-app flows; the API tests run entirely against the local mock — no real Verkada API traffic is generated.

## Setup

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e .
playwright install chromium
cp .env.example .env
# edit .env with your trial-account email, password, TOTP secret, and org URL
```

## Run

```bash
# UI suite (headed Chromium against command.verkada.com)
pytest tests/ui

# Mock-API suite (FastAPI mock, no network)
pytest tests/mock_api

# Everything
pytest

# Lint
ruff check .
```

## Status

Scaffold only. Built so far:

- `pyproject.toml` with pinned deps, ruff + pytest config
- `conftest.py` with `verkada_creds`, `playwright_page`, `totp_code` fixtures
- Empty `tests/ui/`, `tests/ui/pages/`, `tests/mock_api/`, `mocks/` directories
- `README.md`, `LIMITATIONS.md`

Not yet built: page objects, UI tests, mock server, mock-API tests.

## Limitations

See [LIMITATIONS.md](LIMITATIONS.md).
