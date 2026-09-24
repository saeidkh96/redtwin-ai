from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4


class EventStore:
    def __init__(self) -> None:
        self._events: list[dict[str, object]] = []

    def publish(self, event_type: str, payload: dict[str, object]) -> dict[str, object]:
        event = {
            "id": str(uuid4()),
            "specversion": "1.0",
            "source": "redtwin-ai",
            "type": event_type,
            "time": datetime.now(UTC).isoformat(),
            "data": payload,
        }
        self._events.append(event)
        return event

    def recent(self) -> list[dict[str, object]]:
        return self._events[-50:]


def capability_document() -> dict[str, object]:
    return {
        "project": "redtwin-ai",
        "version": "1.0.0",
        "protocol": "rednexus_capability_v1",
        "capabilities": [
            {"name": "redtwin.state.read", "mode": "http", "path": "/v1/twin/state"},
            {"name": "redtwin.scenario.run", "mode": "http", "path": "/v1/scenarios/run", "approval_required": True},
            {"name": "redtwin.insights.read", "mode": "http", "path": "/v1/insights"},
        ],
        "events": ["redtwin.tick.completed", "redtwin.scenario.completed"],
    }
