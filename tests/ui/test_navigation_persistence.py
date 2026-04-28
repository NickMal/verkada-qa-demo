"""UI smoke test: authenticated session persists across a hard refresh.

Navigates to a deep page (/devices/add), reloads, and verifies the user
is still authenticated on the same page rather than bounced to /login.
Catches regressions in cookie scoping, SPA auth-state hydration, and
client-side route restoration.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING
from urllib.parse import urlparse

from playwright.sync_api import expect

from tests.ui.pages.login_page import LoginPage

if TYPE_CHECKING:
    from playwright.sync_api import Page

    from conftest import VerkadaCreds


def test_navigation_persists_after_refresh(
    login_page: LoginPage,
    playwright_page: Page,
    verkada_creds: VerkadaCreds,
    totp_code: Callable[[], str],
) -> None:
    login_page.goto()
    login_page.fill_email(verkada_creds.email)
    login_page.fill_password(verkada_creds.password)
    login_page.submit_credentials()
    login_page.fill_totp(totp_code())
    assert login_page.is_logged_in() is True

    # Session is bound to the org subdomain; build the URL from the live origin.
    origin = urlparse(playwright_page.url)
    devices_add_url = f"{origin.scheme}://{origin.netloc}/devices/add"
    playwright_page.goto(devices_add_url)

    expect(playwright_page.get_by_text("Add Devices")).to_be_visible(timeout=10_000)
    assert "/devices/add" in playwright_page.url

    playwright_page.reload()

    assert "/devices/add" in playwright_page.url
    assert "/login" not in playwright_page.url
    expect(playwright_page.get_by_text("Add Devices")).to_be_visible(timeout=10_000)
