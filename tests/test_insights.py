from redtwin.insights import InsightService
from redtwin.runtime import TwinRuntime
from redtwin.scenarios import ScenarioEngine


def test_critical_insight_is_explainable() -> None:
    runtime = TwinRuntime()
    runtime.tick()
    ScenarioEngine().run(runtime, "vibration_spike", "press-01")
    findings = InsightService().evaluate(runtime)
    assert findings[0]["risk_score"] >= 70
    assert "vibration" in findings[0]["explanation"]
