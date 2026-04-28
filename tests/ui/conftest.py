"""UI-test-scoped fixtures."""

from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING
from urllib.parse import urlparse

import pyotp
import pytest

from tests.ui.pages.login_page import LoginPage

if TYPE_CHECKING:
    from playwright.sync_api import BrowserContext, Page, Playwright

    from conftest import VerkadaCreds


@pytest.fixture
def login_page(playwright_page: Page, verkada_creds: VerkadaCreds) -> LoginPage:
    return LoginPage(page=playwright_page, base_url=verkada_creds.org_url)


@pytest.fixture(scope="session")
def authenticated_context(
    session_playwright: Playwright,
    verkada_creds: VerkadaCreds,
) -> Iterator[BrowserContext]:
    browser = session_playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    login = LoginPage(page=page, base_url=verkada_creds.org_url)
    login.goto()
    login.fill_email(verkada_creds.email)
    login.fill_password(verkada_creds.password)
    login.submit_credentials()
    login.fill_totp(pyotp.TOTP(verkada_creds.totp_secret).now())
    if not login.is_logged_in():
        raise RuntimeError(
            "Session login failed during fixture setup — "
            "likely TOTP timing collision or selector regression."
        )
    # Leave the initial page open: downstream fixtures read its URL to discover
    # the post-login origin (org-specific subdomain) without re-parsing creds.

    try:
        yield context
    finally:
        context.close()
        browser.close()


@pytest.fixture
def authenticated_page(authenticated_context: BrowserContext) -> Iterator[Page]:
    initial_page = authenticated_context.pages[0]
    parsed = urlparse(initial_page.url)
    origin = f"{parsed.scheme}://{parsed.netloc}"

    page = authenticated_context.new_page()
    page.goto(origin)
    try:
        yield page
    finally:
        page.close()
