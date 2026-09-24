from redtwin.domain import MachineStatus
from redtwin.runtime import TwinRuntime, create_factory


def test_factory_has_five_machines() -> None:
    assert len(create_factory().machines) == 5


def test_tick_populates_operational_telemetry() -> None:
    runtime = TwinRuntime()
    state = runtime.tick(2)
    assert state["tick"] == 2
    assert state["kpis"]["total_energy_kw"] > 0
    assert all(item["status"] == MachineStatus.RUNNING.value for item in state["machines"])


def test_tick_rejects_invalid_step_count() -> None:
    runtime = TwinRuntime()
    try:
        runtime.tick(0)
    except ValueError as error:
        assert "steps" in str(error)
    else:
        raise AssertionError("expected validation error")
