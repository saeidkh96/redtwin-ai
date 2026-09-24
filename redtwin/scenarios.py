from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from redtwin.domain import MachineStatus
from redtwin.runtime import TwinRuntime


@dataclass(frozen=True)
class ScenarioResult:
    name: str
    target_machine: str
    outcome: str
    state: dict[str, object]


class ScenarioEngine:
    supported: ClassVar[set[str]] = {"overload", "cooling_failure", "vibration_spike", "recovery"}

    def run(self, runtime: TwinRuntime, name: str, machine_id: str) -> ScenarioResult:
        if name not in self.supported:
            raise ValueError(f"unsupported scenario: {name}")
        machine = runtime.machine(machine_id)
        if name == "overload":
            machine.energy_kw = round(max(machine.energy_kw, 10) * 1.45, 2)
            machine.temperature_c += 18
            machine.throughput_units_h *= 1.12
            machine.status = MachineStatus.DEGRADED
            outcome = "load increased; thermal risk elevated"
        elif name == "cooling_failure":
            machine.temperature_c += 32
            machine.health_score = max(0, machine.health_score - 35)
            machine.status = MachineStatus.DEGRADED
            outcome = "cooling unavailable; intervention recommended"
        elif name == "vibration_spike":
            machine.vibration_mm_s += 5.5
            machine.health_score = max(0, machine.health_score - 30)
            machine.status = MachineStatus.DEGRADED
            outcome = "abnormal vibration detected; inspect mechanical components"
        else:
            machine.temperature_c = 32
            machine.vibration_mm_s = 0.8
            machine.energy_kw = 3.0
            machine.throughput_units_h = 0.0
            machine.health_score = min(100, machine.health_score + 25)
            machine.status = MachineStatus.IDLE
            outcome = "controlled recovery completed"
        return ScenarioResult(name, machine_id, outcome, runtime.factory.snapshot())
