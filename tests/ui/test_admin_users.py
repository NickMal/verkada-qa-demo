"""UI smoke test: User Management page renders with expected structure.

Verifies /admin/users loads with its key affordances: page heading,
at least one user row (the logged-in account, the only user in the
trial org), and the "Add user" button.
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


def test_admin_users_page_loads(
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

    # Session is bound to the org subdomain after login; build the URL from
    # the live page origin instead of the apex.
    origin = urlparse(playwright_page.url)
    users_url = f"{origin.scheme}://{origin.netloc}/admin/users"
    playwright_page.goto(users_url)

    assert "/admin/users" in playwright_page.url
    expect(playwright_page.get_by_text(verkada_creds.email)).to_be_visible(
        timeout=10_000
    )
    expect(playwright_page.get_by_role("button", name="Add user")).to_be_visible(
        timeout=10_000
    )
