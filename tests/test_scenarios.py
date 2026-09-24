from redtwin.domain import MachineStatus
from redtwin.runtime import TwinRuntime
from redtwin.scenarios import ScenarioEngine


def test_cooling_failure_degrades_machine() -> None:
    runtime = TwinRuntime()
    runtime.tick()
    result = ScenarioEngine().run(runtime, "cooling_failure", "mixer-01")
    machine = next(item for item in result.state["machines"] if item["id"] == "mixer-01")
    assert machine["status"] == MachineStatus.DEGRADED.value
    assert machine["temperature_c"] > 70


def test_recovery_returns_machine_to_idle() -> None:
    runtime = TwinRuntime()
    ScenarioEngine().run(runtime, "recovery", "mixer-01")
    assert runtime.machine("mixer-01").status == MachineStatus.IDLE
