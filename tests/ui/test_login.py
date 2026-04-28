"""UI tests: successful login to Verkada Command with TOTP, and invalid-password rejection."""

from __future__ import annotations

from typing import TYPE_CHECKING
from collections.abc import Callable

from tests.ui.pages.login_page import LoginPage

if TYPE_CHECKING:
    from conftest import VerkadaCreds


def test_login_success(
    login_page: LoginPage,
    verkada_creds: VerkadaCreds,
    totp_code: Callable[[], str],
) -> None:
    login_page.goto()
    login_page.fill_email(verkada_creds.email)
    login_page.fill_password(verkada_creds.password)
    login_page.submit_credentials()
    login_page.fill_totp(totp_code())
    assert login_page.is_logged_in() is True


def test_login_invalid_password(
    login_page: LoginPage,
    verkada_creds: VerkadaCreds,
) -> None:
    login_page.goto()
    login_page.fill_email(verkada_creds.email)
    login_page.fill_password("wrong-password-123")
    login_page.submit_credentials()
    assert login_page.is_credentials_error_visible() is True
    assert login_page.is_logged_in() is False
