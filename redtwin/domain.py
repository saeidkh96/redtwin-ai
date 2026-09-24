from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum


class MachineStatus(StrEnum):
    IDLE = "idle"
    RUNNING = "running"
    DEGRADED = "degraded"
    FAILED = "failed"


@dataclass
class Machine:
    id: str
    name: str
    status: MachineStatus = MachineStatus.IDLE
    temperature_c: float = 25.0
    vibration_mm_s: float = 0.5
    energy_kw: float = 0.0
    throughput_units_h: float = 0.0
    health_score: float = 100.0

    def snapshot(self) -> dict[str, object]:
        result = asdict(self)
        result["status"] = self.status.value
        return result


@dataclass
class FactoryTwin:
    id: str = "genesis-factory-01"
    tick: int = 0
    machines: list[Machine] = field(default_factory=list)

    @property
    def total_energy_kw(self) -> float:
        return round(sum(machine.energy_kw for machine in self.machines), 2)

    @property
    def total_throughput_units_h(self) -> float:
        return round(sum(machine.throughput_units_h for machine in self.machines), 2)

    def snapshot(self) -> dict[str, object]:
        return {
            "factory_id": self.id,
            "tick": self.tick,
            "kpis": {
                "total_energy_kw": self.total_energy_kw,
                "total_throughput_units_h": self.total_throughput_units_h,
                "available_machines": sum(m.status != MachineStatus.FAILED for m in self.machines),
                "machine_count": len(self.machines),
            },
            "machines": [machine.snapshot() for machine in self.machines],
        }
