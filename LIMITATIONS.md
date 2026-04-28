# Limitations

Known limits of this demo. Be explicit about these in any walkthrough.

- **No real device access.** The demo does not talk to physical Verkada cameras, access controllers, or any other hardware. Tests only touch web UI and a local mock server.
- **No mobile testing.** Coverage is desktop Chromium only via Playwright. The Verkada mobile apps and mobile-web breakpoints are out of scope.
- **Mock-only API simulation.** The FastAPI server under `mocks/` simulates a thin slice of the public Verkada API surface (token mint, a handful of read endpoints) for demo purposes. It is not a faithful reproduction of real API behavior, error semantics, rate limits, or pagination edge cases — and it never sends traffic to `api.verkada.com`.
- **CI flakiness disclosure.** The GitHub Actions workflow runs the UI suite with `continue-on-error: true`. Cloud login flows (Verkada or otherwise) can introduce anti-automation challenges — CAPTCHAs, device-trust prompts, IP-based step-up — that are inherently flaky from CI runners. Failures there should be inspected manually rather than auto-blocking the build. The mock-API suite does not have this carve-out and must pass cleanly.
