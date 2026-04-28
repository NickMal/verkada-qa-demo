"""Tests for the POST /webhook/access-event mock endpoint."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi.testclient import TestClient


def test_webhook_event_payload_validation(mock_client: TestClient) -> None:
    valid_payload = {
        "event_id": "evt-mock-001",
        "door_id": "door-mock-1",
        "user_id": "user-mock-1",
        "timestamp": "2025-04-27T12:00:00Z",
        "event_type": "unlock",
    }

    ok_response = mock_client.post("/webhook/access-event", json=valid_payload)
    assert ok_response.status_code == 200
    body = ok_response.json()
    assert body["status"] == "received"
    assert body["event_id"] == "evt-mock-001"

    malformed_payload = {k: v for k, v in valid_payload.items() if k != "event_type"}
    bad_response = mock_client.post("/webhook/access-event", json=malformed_payload)
    assert bad_response.status_code == 422
