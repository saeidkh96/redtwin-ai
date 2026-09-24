# RedNexus Integration

RedTwin remains an independent service. RedNexus discovers `/v1/capabilities` and invokes only declared capabilities.

| Capability | Effect | Approval |
|---|---|---|
| `redtwin.state.read` | Returns twin state | No |
| `redtwin.insights.read` | Returns explainable findings | No |
| `redtwin.scenario.run` | Mutates simulated state | Yes |

Events use a CloudEvents-compatible envelope. `redtwin.scenario.completed` can trigger a RedPA explanation workflow or a RedPulse maintenance evaluation, with human approval governed by RedNexus.
