# Limitations

Known limits of this demo. Be explicit about these in any walkthrough.

- **No real device access.** The demo does not talk to physical Verkada cameras, access controllers, or any other hardware. Tests only touch web UI and a local mock server.
- **No mobile testing.** Coverage is desktop Chromium only via Playwright. The Verkada mobile apps and mobile-web breakpoints are out of scope.
- **Mock-only API simulation.** The FastAPI server under `mocks/` simulates a thin slice of the public Verkada API surface (token mint, a handful of read endpoints) for demo purposes. It is not a faithful reproduction of real API behavior, error semantics, rate limits, or pagination edge cases — and it never sends traffic to `api.verkada.com`.
- **CI flakiness disclosure.** The GitHub Actions workflow runs the UI suite with `continue-on-error: true`. Cloud login flows (Verkada or otherwise) can introduce anti-automation challenges — CAPTCHAs, device-trust prompts, IP-based step-up — that are inherently flaky from CI runners. Failures there should be inspected manually rather than auto-blocking the build. The mock-API suite does not have this carve-out and must pass cleanly.

## UI Suite Authentication Model

The UI suite uses a session-scoped authenticated browser context: one login per pytest session, shared across all tests that need an authenticated page. This is an intentional architectural choice driven by two constraints:

1. **TOTP single-use enforcement** — Verkada correctly rejects reuse of the same TOTP code within its 30-second validity window (RFC 6238 §5.2). Per-test login would cause collisions in full-suite runs.

2. **Test independence is preserved at the page level** — each test creates a fresh page from the shared context via `context.new_page()`, performs its own navigation, and asserts against its own page state. Tests do not share page state, only the authenticated session.

The login flow itself remains tested via `test_login_success` and `test_login_invalid_password`, which use a fresh unauthenticated browser context (the `playwright_page` fixture).

In a production environment with a dedicated test tenant, this constraint could be removed by issuing per-test service-account credentials or a TOTP-bypass mechanism for automated testing.

> The single test that performs a fresh login (test_login_success) waits 31 seconds at the start to ensure a TOTP window separation from the session-scoped login fixture. This is an explicit, isolated wait — not a retry mechanism or test-ordering hack — and adds ~31s to full-suite runtime.
