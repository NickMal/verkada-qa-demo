"""Root conftest: env loading and shared fixtures for UI and mock-API tests."""

from __future__ import annotations

import os
from collections.abc import Callable, Iterator

import pyotp
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, Playwright, sync_playwright
from pydantic import BaseModel

load_dotenv()


class VerkadaCreds(BaseModel):
    email: str
    password: str
    totp_secret: str
    org_url: str


@pytest.fixture(scope="session")
def verkada_creds() -> VerkadaCreds:
    required = {
        "email": os.getenv("VERKADA_EMAIL"),
        "password": os.getenv("VERKADA_PASSWORD"),
        "totp_secret": os.getenv("VERKADA_TOTP_SECRET"),
        "org_url": os.getenv("VERKADA_ORG_URL"),
    }
    missing = [k for k, v in required.items() if not v]
    if missing:
        raise RuntimeError(
            f"Missing required env vars for Verkada creds: {missing}. "
            "Copy .env.example to .env and fill in values."
        )
    return VerkadaCreds(**required)  # type: ignore[arg-type]


@pytest.fixture(scope="session")
def session_playwright() -> Iterator[Playwright]:
    # Single Playwright instance per pytest session. sync_playwright owns its
    # asyncio loop; spinning up a second instance while one is alive raises
    # "Sync API inside the asyncio loop", so all browser fixtures share this.
    pw = sync_playwright().start()
    try:
        yield pw
    finally:
        pw.stop()


@pytest.fixture
def playwright_page(session_playwright: Playwright) -> Iterator[Page]:
    browser = session_playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    try:
        yield page
    finally:
        context.close()
        browser.close()


@pytest.fixture
def totp_code(verkada_creds: VerkadaCreds) -> Callable[[], str]:
    def _generate() -> str:
        return pyotp.TOTP(verkada_creds.totp_secret).now()

    return _generate
