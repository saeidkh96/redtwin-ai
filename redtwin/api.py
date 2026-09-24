from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from redtwin import __version__
from redtwin.events import EventStore, capability_document
from redtwin.insights import InsightService
from redtwin.runtime import TwinRuntime
from redtwin.scenarios import ScenarioEngine

app = FastAPI(title="RedTwin AI", version=__version__, description="Smart Factory Digital Twin")
runtime = TwinRuntime()
scenarios = ScenarioEngine()
insights = InsightService()
events = EventStore()


class TickRequest(BaseModel):
    steps: int = Field(default=1, ge=1, le=100)


class ScenarioRequest(BaseModel):
    name: str
    machine_id: str


@app.get("/health")
def health() -> dict[str, object]:
    return {"status": "ok", "service": "redtwin-ai", "version": __version__}


@app.get("/v1/twin/state")
def state() -> dict[str, object]:
    return runtime.factory.snapshot()


@app.post("/v1/twin/tick")
def tick(request: TickRequest) -> dict[str, object]:
    result = runtime.tick(request.steps)
    events.publish("redtwin.tick.completed", {"factory_id": runtime.factory.id, "tick": runtime.factory.tick})
    return result


@app.post("/v1/scenarios/run")
def run_scenario(request: ScenarioRequest) -> dict[str, object]:
    try:
        result = scenarios.run(runtime, request.name, request.machine_id)
    except (KeyError, ValueError) as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    response = {"name": result.name, "target_machine": result.target_machine, "outcome": result.outcome, "state": result.state}
    events.publish("redtwin.scenario.completed", response)
    return response


@app.get("/v1/insights")
def get_insights() -> dict[str, object]:
    return {"factory_id": runtime.factory.id, "insights": insights.evaluate(runtime)}


@app.get("/v1/capabilities")
def capabilities() -> dict[str, object]:
    return capability_document()


@app.get("/v1/events")
def get_events() -> dict[str, object]:
    return {"events": events.recent()}


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def dashboard() -> str:
    return '''<!doctype html><html><head><meta charset="utf-8"><title>RedTwin AI</title>
<style>body{font-family:system-ui;background:#101217;color:#edf0f5;max-width:1100px;margin:40px auto;padding:0 20px}h1 b{color:#f04444}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px}.card{background:#1c2029;border:1px solid #303746;border-radius:12px;padding:16px}.bad{color:#ff6b6b}.ok{color:#59d69d}button,select{padding:10px;border-radius:7px;border:0;margin-right:8px}pre{white-space:pre-wrap;background:#171a21;padding:15px;border-radius:10px}</style></head>
<body><h1><b>Red</b>Twin AI <small>v1.0.0</small></h1><p>Smart Factory Digital Twin — simulate, inspect, decide.</p>
<button onclick="tick()">Advance Tick</button><select id="scenario"><option value="overload">Overload</option><option value="cooling_failure">Cooling failure</option><option value="vibration_spike">Vibration spike</option><option value="recovery">Recovery</option></select><button onclick="runScenario()">Run Scenario on mixer</button>
<h2>Factory State</h2><div class="grid" id="machines"></div><h2>AI Insights</h2><pre id="insights">Loading…</pre>
<script>async function load(){let s=await fetch('/v1/twin/state').then(r=>r.json());document.querySelector('#machines').innerHTML=s.machines.map(m=>`<div class="card"><b>${m.name}</b><p class="${m.status==='degraded'?'bad':'ok'}">${m.status}</p><small>${m.temperature_c}°C · ${m.vibration_mm_s} mm/s<br>${m.energy_kw} kW · Health ${m.health_score}</small></div>`).join('');let i=await fetch('/v1/insights').then(r=>r.json());document.querySelector('#insights').textContent=i.insights.length?JSON.stringify(i.insights,null,2):'No anomalies detected.'}async function tick(){await fetch('/v1/twin/tick',{method:'POST',headers:{'Content-Type':'application/json'},body:'{"steps":1}'});load()}async function runScenario(){await fetch('/v1/scenarios/run',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:document.querySelector('#scenario').value,machine_id:'mixer-01'})});load()}load()</script></body></html>'''
