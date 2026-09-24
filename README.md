# RedTwin AI

> **Source-available for non-commercial use. Not open source.** See [LICENSE](LICENSE).

**RedTwin AI** is a Smart Factory Digital Twin. It maintains a simulated operational state, runs deterministic what-if scenarios, explains operational risk, and publishes integration-ready events for the RedNexus ecosystem.

RedTwin is the simulation and explanation layer of the Red ecosystem. Its current risk logic is rule-based and fully traceable. Learned models, such as predictive maintenance from RedPulse, connect through versioned contracts rather than being built into the twin.

## v1.0.0 capabilities

- Five-machine factory model with temperature, vibration, energy, throughput and health telemetry
- Deterministic tick runtime with state transitions: `idle`, `running`, `degraded`, `failed`
- What-if scenarios: overload, cooling failure, vibration spike and recovery
- Rule-based, explainable risk and anomaly insights
- FastAPI REST API and a dependency-free web dashboard
- Versioned RedNexus capability/event contract
- Docker, CI, tests and release evidence

## How risk is scored

Every insight can be traced to a threshold, so there are no black-box scores.

| Signal | Condition | Risk added |
|---|---|---|
| Temperature | 70 °C or higher | +40 |
| Vibration | 4 mm/s or higher | +50 |
| Machine status | `degraded` or `failed` | +25 |

A total of 70 or more is **critical**; anything above zero is a **warning**. Scores are capped at 100. Each insight states its causes, for example *"Risk is driven by temperature 74°C, vibration 5.1 mm/s."*

This is deliberate for v1.0.0: a deterministic twin with transparent rules is testable and gives learned models a stable baseline to be compared against.

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

RedTwin AI is released under the **RedTwin AI Source-Available License 1.0**.

You may view, study, download, run and privately modify it for personal, educational, research and other non-commercial purposes. Commercial use, including use inside a business to operate, monitor or analyse real facilities, requires a separate written license.

RedTwin produces simulated outputs only. It is not designed or certified for controlling or making decisions about real machinery. See [LICENSE](LICENSE) for the full terms.
