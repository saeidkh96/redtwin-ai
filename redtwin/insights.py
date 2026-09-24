from __future__ import annotations

from dataclasses import asdict, dataclass

from redtwin.domain import MachineStatus
from redtwin.runtime import TwinRuntime


@dataclass(frozen=True)
class Insight:
    machine_id: str
    severity: str
    risk_score: int
    title: str
    explanation: str
    recommendation: str


class InsightService:
    def evaluate(self, runtime: TwinRuntime) -> list[dict[str, object]]:
        insights: list[Insight] = []
        for machine in runtime.factory.machines:
            risk = 0
            causes: list[str] = []
            if machine.temperature_c >= 70:
                risk += 40
                causes.append(f"temperature {machine.temperature_c}°C")
            if machine.vibration_mm_s >= 4:
                risk += 50
                causes.append(f"vibration {machine.vibration_mm_s} mm/s")
            if machine.status in {MachineStatus.DEGRADED, MachineStatus.FAILED}:
                risk += 25
                causes.append(f"status {machine.status.value}")
            if risk:
                severity = "critical" if risk >= 70 else "warning"
                insights.append(Insight(
                    machine.id, severity, min(risk, 100), "Operational anomaly",
                    "Risk is driven by " + ", ".join(causes) + ".",
                    "Schedule inspection and evaluate the recovery scenario.",
                ))
        return [asdict(item) for item in sorted(insights, key=lambda x: x.risk_score, reverse=True)]
