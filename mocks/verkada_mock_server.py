"""Mock server simulating Verkada Cloud API response shapes. NOT a real Verkada integration."""

from __future__ import annotations

import logging
import sys
from datetime import datetime
from typing import Literal

import uvicorn
from fastapi import FastAPI, Request
from pydantic import BaseModel, ConfigDict

_LOG_PREFIX = "[MOCK SERVER]"

logger = logging.getLogger("mock_server")
logger.setLevel(logging.INFO)
if not logger.handlers:
    _handler = logging.StreamHandler(sys.stderr)
    _handler.setFormatter(logging.Formatter(f"{_LOG_PREFIX} %(message)s"))
    logger.addHandler(_handler)


class Camera(BaseModel):
    camera_id: str
    name: str
    site: str
    status: Literal["online", "offline"]
    firmware: str


class CameraInfoResponse(BaseModel):
    cameras: list[Camera]


class AccessEvent(BaseModel):
    # strict validation: incoming payload contract
    model_config = ConfigDict(extra="forbid")

    event_id: str
    door_id: str
    user_id: str
    timestamp: datetime
    event_type: Literal["unlock", "denied", "forced_open"]


FLEET: list[Camera] = [
    Camera(
        camera_id="cam-mock-001",
        name="Test Camera 1",
        site="Mock Site A",
        status="online",
        firmware="1.0.0-mock",
    ),
    Camera(
        camera_id="cam-mock-002",
        name="Test Camera 2",
        site="Mock Site A",
        status="online",
        firmware="1.0.0-mock",
    ),
    Camera(
        camera_id="cam-mock-003",
        name="Test Camera 3",
        site="Mock Site B",
        status="offline",
        firmware="0.9.7-mock",
    ),
    Camera(
        camera_id="cam-mock-004",
        name="Test Camera 4",
        site="Mock Site B",
        status="online",
        firmware="1.0.0-mock",
    ),
    Camera(
        camera_id="cam-mock-005",
        name="Test Camera 5",
        site="Mock Site C",
        status="online",
        firmware="1.0.0-mock",
    ),
]


app = FastAPI(title="Mock API (shape simulation only)")


@app.middleware("http")
# FastAPI middleware signature; call_next type lives in private starlette types
async def log_requests(request: Request, call_next):  # type: ignore[no-untyped-def]
    logger.info("%s %s", request.method, request.url.path)
    return await call_next(request)


@app.get("/camera/v1/info", response_model=CameraInfoResponse)
def get_camera_info() -> CameraInfoResponse:
    return CameraInfoResponse(cameras=FLEET)


@app.post("/webhook/access-event")
def post_access_event(event: AccessEvent) -> dict[str, str]:
    return {"status": "received", "event_id": event.event_id}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8765)
