"""Tests for the GET /camera/v1/info mock endpoint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from mocks.verkada_mock_server import CameraInfoResponse

if TYPE_CHECKING:
    from fastapi.testclient import TestClient


def test_camera_info_returns_fleet(mock_client: TestClient) -> None:
    response = mock_client.get("/camera/v1/info")
    assert response.status_code == 200
    parsed = CameraInfoResponse.model_validate(response.json())
    assert len(parsed.cameras) == 5


def test_camera_info_offline_status(mock_client: TestClient) -> None:
    response = mock_client.get("/camera/v1/info")
    parsed = CameraInfoResponse.model_validate(response.json())
    assert any(camera.status == "offline" for camera in parsed.cameras)
