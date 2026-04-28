"""Page object for the Verkada Command login flow.

Selectors confirmed 2025-04-27 via Playwright codegen against
command.verkada.com. Verkada uses a multi-step login: email screen ->
password screen -> MFA factor chooser -> 6-digit TOTP entry. The TOTP
screen auto-submits once the 6th digit is filled, so there is no
`submit_totp` step.
"""

from __future__ import annotations

from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


class LoginPage:
    """Encapsulates the Verkada Command login + TOTP flow."""

    _TOTP_DIGIT_ORDINALS: tuple[str, ...] = ("1st", "2nd", "3rd", "4th", "5th", "6th")

    def __init__(self, page: Page, base_url: str) -> None:
        self._page = page
        self._base_url = base_url.rstrip("/")

    def goto(self) -> None:
        self._page.goto(self._base_url)

    def fill_email(self, email: str) -> None:
        # confirmed 2025-04-27
        self._page.get_by_role("textbox", name="Email").fill(email)
        # confirmed 2025-04-27 — advances to the password screen
        self._page.get_by_test_id("Account.Login.Email.LogInManually").click()

    def fill_password(self, password: str) -> None:
        # confirmed 2025-04-27
        self._page.get_by_role("textbox", name="Show password Password").fill(password)

    def submit_credentials(self) -> None:
        # confirmed 2025-04-27
        self._page.get_by_test_id("Account.Login.Password.Submit").click()

    def fill_totp(self, code: str) -> None:
        if len(code) != 6 or not code.isdigit():
            raise ValueError(f"TOTP code must be 6 numeric digits, got {code!r}")
        # confirmed 2025-04-27 — choose TOTP factor before entering digits
        self._page.get_by_role("button", name="Authenticator App").click()
        for ordinal, digit in zip(self._TOTP_DIGIT_ORDINALS, code, strict=True):
            # confirmed 2025-04-27
            self._page.get_by_role(
                "textbox", name=f"Enter the {ordinal} digit of the"
            ).fill(digit)
        # Verkada auto-submits once all 6 digits are filled — no explicit submit.

    def is_logged_in(self) -> bool:
        # confirmed 2025-04-27
        try:
            self._page.get_by_test_id("GlobalNav.AccountMenuButton").wait_for(
                state="visible", timeout=10_000
            )
            return True
        except PlaywrightTimeoutError:
            return False
