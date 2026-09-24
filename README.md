# RedTwin AI

**RedTwin AI** is an AI-enabled Smart Factory Digital Twin. It maintains a simulated operational state, runs deterministic what-if scenarios, detects operational risk, and publishes integration-ready events for the RedNexus ecosystem.

## v1.0.0 capabilities

- Five-machine factory model with temperature, vibration, energy, throughput and health telemetry
- Deterministic tick runtime with state transitions: `idle`, `running`, `degraded`, `failed`
- What-if scenarios: overload, cooling failure, vibration spike and recovery
- Explainable risk and anomaly insights
- FastAPI REST API and a dependency-free web dashboard
- Versioned RedNexus capability/event contract
- Docker, CI, tests and release evidence

## Quick start

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m uvicorn redtwin.api:app --reload
```

Open `http://127.0.0.1:8000`. The API docs are at `/docs`.

Run the deterministic CLI demo:

```bash
python -m redtwin.demo
```

Run validation:

```bash
python -m pytest -q
python -m ruff check .
```

## API

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Service health and version |
| GET | `/v1/twin/state` | Current twin state and factory KPIs |
| POST | `/v1/twin/tick` | Advance the simulated factory |
| POST | `/v1/scenarios/run` | Run a what-if scenario |
| GET | `/v1/insights` | Explainable risk/anomaly findings |
| GET | `/v1/capabilities` | RedNexus discovery document |
| GET | `/v1/events` | Recent integration events |

## Ecosystem boundary

RedTwin owns the operational model and scenario simulation. RedPulse can consume telemetry for predictive maintenance; RedPA can explain insights and create approved workflows; RedNexus discovers the service and coordinates versioned events. No project code or database is shared directly.

## License

Source-available portfolio project. See [LICENSE](LICENSE).
