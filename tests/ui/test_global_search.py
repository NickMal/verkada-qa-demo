"""UI smoke test: User Management search input renders and accepts input.

Scope is intentionally narrow: this empty trial org has no users to search,
so we only verify the search field is present on a real authenticated page
and that it accepts a query string. Result rendering is out of scope and
documented in LIMITATIONS.md.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from urllib.parse import urlparse

if TYPE_CHECKING:
    from playwright.sync_api import Page


def test_global_search_input_accepts_query(authenticated_page: Page) -> None:
    origin = urlparse(authenticated_page.url)
    users_url = f"{origin.scheme}://{origin.netloc}/admin/users"
    authenticated_page.goto(users_url)

    # confirmed 2025-04-27
    search_input = authenticated_page.get_by_placeholder("Search...")
    search_input.fill("test query")

    assert search_input.input_value() == "test query"
    assert "/admin/users" in authenticated_page.url
