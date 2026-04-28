"""Fixtures for mock API tests. TestClient injection lives here."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def mock_client() -> TestClient:
    from mocks.verkada_mock_server import app

    return TestClient(app)
