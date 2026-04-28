"""UI-test-scoped fixtures."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from playwright.sync_api import Page

from tests.ui.pages.login_page import LoginPage

if TYPE_CHECKING:
    from conftest import VerkadaCreds


@pytest.fixture
def login_page(playwright_page: Page, verkada_creds: VerkadaCreds) -> LoginPage:
    return LoginPage(page=playwright_page, base_url=verkada_creds.org_url)
