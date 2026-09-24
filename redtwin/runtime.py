from __future__ import annotations

from redtwin.domain import FactoryTwin, Machine, MachineStatus


def create_factory(factory_id: str = "genesis-factory-01") -> FactoryTwin:
    return FactoryTwin(
        id=factory_id,
        machines=[
            Machine("mixer-01", "Raw Material Mixer"),
            Machine("press-01", "Hydraulic Press"),
            Machine("robot-01", "Assembly Robot"),
            Machine("pack-01", "Packaging Line"),
            Machine("hvac-01", "Industrial Cooling"),
        ],
    )


class TwinRuntime:
    """Deterministic simulation runtime; stable by design for tests and demos."""

    def __init__(self, factory: FactoryTwin | None = None) -> None:
        self.factory = factory or create_factory()

    def tick(self, steps: int = 1) -> dict[str, object]:
        if not 1 <= steps <= 100:
            raise ValueError("steps must be between 1 and 100")
        for _ in range(steps):
            self.factory.tick += 1
            for index, machine in enumerate(self.factory.machines):
                self._advance_machine(machine, index)
        return self.factory.snapshot()

    def _advance_machine(self, machine: Machine, index: int) -> None:
        phase = (self.factory.tick + index) % 7
        if machine.status == MachineStatus.FAILED:
            machine.energy_kw = 0.0
            machine.throughput_units_h = 0.0
            machine.temperature_c = max(25.0, machine.temperature_c - 1.2)
            return
        if machine.status == MachineStatus.IDLE:
            machine.status = MachineStatus.RUNNING
        machine.temperature_c = round(49 + index * 1.8 + phase * 0.7, 2)
        machine.vibration_mm_s = round(1.1 + index * 0.13 + phase * 0.06, 2)
        machine.energy_kw = round(8 + index * 2.6 + phase * 0.35, 2)
        machine.throughput_units_h = round(40 - index * 2 + phase, 2)
        machine.health_score = round(max(0.0, 100 - max(0, machine.temperature_c - 65) * 1.7), 2)
        if machine.temperature_c > 72 or machine.vibration_mm_s > 5:
            machine.status = MachineStatus.DEGRADED

    def machine(self, machine_id: str) -> Machine:
        for machine in self.factory.machines:
            if machine.id == machine_id:
                return machine
        raise KeyError(f"unknown machine: {machine_id}")
