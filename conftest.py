"""Root conftest: env loading and shared fixtures for UI and mock-API tests."""

from __future__ import annotations

import os
from collections.abc import Callable, Iterator

import pyotp
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, sync_playwright
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


@pytest.fixture
def playwright_page() -> Iterator[Page]:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
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
