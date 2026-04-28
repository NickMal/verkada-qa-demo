"""UI smoke test: User Management search input renders and accepts input.

Scope is intentionally narrow: this empty trial org has no users to search,
so we only verify the search field is present on a real authenticated page
and that it accepts a query string. Result rendering is out of scope and
documented in LIMITATIONS.md.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING
from urllib.parse import urlparse

from tests.ui.pages.login_page import LoginPage

if TYPE_CHECKING:
    from playwright.sync_api import Page

    from conftest import VerkadaCreds


def test_global_search_input_accepts_query(
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

    # Session is scoped to the org-specific subdomain after login (e.g.
    # <slug>.command.verkada.com). Hitting the apex /admin/users bounces to
    # the login screen, so build the URL from the current page's origin.
    origin = urlparse(playwright_page.url)
    users_url = f"{origin.scheme}://{origin.netloc}/admin/users"
    playwright_page.goto(users_url)

    # confirmed 2025-04-27
    search_input = playwright_page.get_by_placeholder("Search...")
    search_input.fill("test query")

    assert search_input.input_value() == "test query"
    assert "/admin/users" in playwright_page.url
