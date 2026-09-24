from __future__ import annotations

import json

from redtwin.events import EventStore
from redtwin.insights import InsightService
from redtwin.runtime import TwinRuntime
from redtwin.scenarios import ScenarioEngine


def main() -> None:
    runtime = TwinRuntime()
    runtime.tick(3)
    result = ScenarioEngine().run(runtime, "cooling_failure", "mixer-01")
    EventStore().publish("redtwin.scenario.completed", {"name": result.name})
    print(json.dumps({"scenario": result.outcome, "insights": InsightService().evaluate(runtime)}, indent=2))


if __name__ == "__main__":
    main()
