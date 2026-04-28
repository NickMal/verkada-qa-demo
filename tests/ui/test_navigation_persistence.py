"""UI smoke test: authenticated session persists across a hard refresh.

Navigates to a deep page (/devices/add), reloads, and verifies the user
is still authenticated on the same page rather than bounced to /login.
Catches regressions in cookie scoping, SPA auth-state hydration, and
client-side route restoration.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from urllib.parse import urlparse

from playwright.sync_api import expect

if TYPE_CHECKING:
    from playwright.sync_api import Page


def test_navigation_persists_after_refresh(authenticated_page: Page) -> None:
    origin = urlparse(authenticated_page.url)
    devices_add_url = f"{origin.scheme}://{origin.netloc}/devices/add"
    authenticated_page.goto(devices_add_url)

    expect(authenticated_page.get_by_text("Add Devices")).to_be_visible(timeout=10_000)
    assert "/devices/add" in authenticated_page.url

    authenticated_page.reload()
    authenticated_page.wait_for_load_state("networkidle")

    assert "/devices/add" in authenticated_page.url
    assert "/login" not in authenticated_page.url
    expect(authenticated_page.get_by_text("Add Devices")).to_be_visible(timeout=10_000)
