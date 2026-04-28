# Verkada QA Demo

UI test automation against Verkada Command and contract testing of mocked Verkada Cloud API endpoints.

## What this is

A 2-day take-home project demonstrating a thin, honest slice of QA practice: a Playwright UI suite that drives headed Chromium against a real Verkada trial org (TOTP-protected login over `command.verkada.com`), plus a FastAPI mock server that simulates Verkada Cloud API response shapes for in-process contract tests. Scope is intentionally narrow — five UI tests across the auth flow and three read pages, three contract tests against the mock — chosen to demonstrate quality and reliability decisions over breadth. The 2-day budget is the relevant constraint when calibrating depth.

## Quick start

```bash
git clone https://github.com/NickMal/verkada-qa-demo.git
cd verkada-qa-demo
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e . && playwright install chromium
cp .env.example .env  # then fill in VERKADA_EMAIL, VERKADA_PASSWORD, VERKADA_TOTP_SECRET, VERKADA_ORG_URL
pytest tests/
```

Expected: 8 tests pass in ~80 seconds.

> **Note on credentials:** UI tests require a Verkada Command account (email, password, TOTP secret, org URL) in `.env`. To run only the mock API suite without credentials:
>
> ```bash
> pytest tests/mock_api/
> ```
>
> Expected: 3 tests pass in under 100ms.

## What's tested

### UI suite (5 tests, Playwright + Chromium against real Verkada Command)

- `tests/ui/test_login.py::test_login_success` — valid credentials + TOTP land on Command home.
- `tests/ui/test_login.py::test_login_invalid_password` — wrong password shows error, no navigation.
- `tests/ui/test_global_search.py::test_global_search_input_accepts_query` — search input on `/admin/users` renders and accepts text.
- `tests/ui/test_admin_users.py::test_admin_users_page_loads` — User Management page renders with the logged-in user visible.
- `tests/ui/test_navigation_persistence.py::test_navigation_persists_after_refresh` — session and page state survive a hard reload on `/devices/add`.

### Mock API suite (3 tests, FastAPI TestClient, in-process)

- `tests/mock_api/test_camera_info.py::test_camera_info_returns_fleet` — `GET /camera/v1/info` returns a 5-camera fleet matching the pydantic schema.
- `tests/mock_api/test_camera_info.py::test_camera_info_offline_status` — at least one camera in the fleet has `status="offline"`.
- `tests/mock_api/test_webhook_validation.py::test_webhook_event_payload_validation` — `POST /webhook/access-event` validates payload (200 on valid, 422 on malformed).

## Architecture decisions

- **Session-scoped authenticated browser context** rather than per-test login. Verkada enforces TOTP single-use within its 30-second window (RFC 6238 §5.2); per-test login causes collisions when more than one test runs inside the same window. One login per pytest session, one fresh page per test via `context.new_page()`.
- **FastAPI `TestClient` instead of running uvicorn** for the mock-API suite. In-process, deterministic, no port binding, no startup/teardown. The full 3-test suite runs in under 100ms.
- **Pydantic v2 schema asymmetry.** Incoming request models use `extra="forbid"` (the mock owns the contract for what it accepts). Outgoing response models leave the default lenient `extra="ignore"`, so the schema tolerates real-API drift if used as a reference.
- **Page Object Model only where it earns its keep.** `LoginPage` exists because two tests exercise the login flow and the multi-step email-then-password-then-TOTP screens benefit from encapsulation. The other UI tests use inline locators because each page is touched by exactly one test.
- **Selectors prefer `get_by_label` / `get_by_role` / `get_by_text` over CSS.** Each confirmed locator carries a `# confirmed 2026-04-27` comment so the source of truth is visible at the call site.

## Limitations and scope

See [LIMITATIONS.md](LIMITATIONS.md) for known constraints (no real device access, no mobile testing, mock API is intentionally not a faithful Verkada simulation, CI uses `continue-on-error` on the UI suite, and the architectural rationale for the session-scoped login model).

## Tech stack

Python 3.12 · pytest · Playwright (Chromium) · httpx · pydantic v2 · FastAPI · uvicorn · ruff · python-dotenv · pyotp

## Project layout

```
.
├── .env.example
├── .github
│   └── workflows
│       └── ci.yml
├── .gitignore
├── CLAUDE.md
├── LIMITATIONS.md
├── README.md
├── conftest.py
├── mocks
│   └── verkada_mock_server.py
├── pyproject.toml
└── tests
    ├── mock_api
    │   ├── conftest.py
    │   ├── test_camera_info.py
    │   └── test_webhook_validation.py
    └── ui
        ├── conftest.py
        ├── pages
        │   └── login_page.py
        ├── test_admin_users.py
        ├── test_global_search.py
        ├── test_login.py
        └── test_navigation_persistence.py
```
