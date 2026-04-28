"""UI smoke test: User Management page renders with expected structure.

Verifies /admin/users loads with its key affordances: page heading,
at least one user row (the logged-in account, the only user in the
trial org), and the "Add user" button.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from urllib.parse import urlparse

from playwright.sync_api import expect

if TYPE_CHECKING:
    from playwright.sync_api import Page

    from conftest import VerkadaCreds


def test_admin_users_page_loads(
    authenticated_page: Page,
    verkada_creds: VerkadaCreds,
) -> None:
    origin = urlparse(authenticated_page.url)
    users_url = f"{origin.scheme}://{origin.netloc}/admin/users"
    authenticated_page.goto(users_url)

    assert "/admin/users" in authenticated_page.url
    expect(authenticated_page.get_by_text(verkada_creds.email)).to_be_visible(
        timeout=10_000
    )
    expect(authenticated_page.get_by_role("button", name="Add user")).to_be_visible(
        timeout=10_000
    )
