# Verkada QA Demo — Agent Instructions

## Goal
Build a 2-day interview demo: 1 Playwright UI suite (5–8 tests) against Verkada Command + 1 FastAPI mock server (3 tests). Nothing more.

## Hard rules — do not
- Attack, scan, or reverse-engineer Verkada systems
- Use private Verkada APIs or undocumented endpoints
- Bypass auth or claim access to real Verkada devices
- Hardcode credentials anywhere; use .env only
- Expand scope beyond the two deliverables above
- Use @pytest.skip to hide failures

## Hard rules — do
- Treat the mock server as clearly mock (filenames, log lines, README all say "mock")
- Public docs only: apidocs.verkada.com and command.verkada.com user-facing UI
- Type hints on all public functions
- Each test independent and deterministic
- If a requirement is ambiguous, STOP and ask before coding

## Stack (locked, no alternatives)
Python 3.12, pytest, Playwright (Chromium only), httpx, pydantic, FastAPI + uvicorn for the mock, ruff for lint, python-dotenv for env loading.

## File layout (locked)

    verkada-qa-demo/
    ├── CLAUDE.md
    ├── README.md
    ├── LIMITATIONS.md
    ├── pyproject.toml
    ├── .env.example
    ├── .gitignore
    ├── conftest.py
    ├── tests/
    │   ├── ui/
    │   │   ├── pages/
    │   │   │   └── login_page.py
    │   │   └── test_*.py
    │   └── mock_api/
    │       └── test_*.py
    ├── mocks/
    │   └── verkada_mock_server.py
    └── .github/workflows/ci.yml

## Operating mode
- Build sequentially: UI suite first, then mock server.
- One test at a time. After each: run `pytest <path> && ruff check`. Stop and show output before continuing.
- Don't generate the entire suite in one shot.

## Definition of done
- All tests pass twice in a row
- ruff clean
- README explains what runs, how to run, what's mocked
- LIMITATIONS.md lists: no real device access, no mobile, mock-only API simulation, CI flakiness disclosure
- .env not committed; .env.example committed

## Verkada API quick facts
- Base: https://api.verkada.com
- Auth: API key → POST to token endpoint → 30-min bearer token
- Tokens cannot be refreshed; re-mint on 401
- Rate limited
- Public docs: https://apidocs.verkada.com