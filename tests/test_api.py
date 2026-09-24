from redtwin.api import app


def test_api_exposes_v1_contract_routes() -> None:
    paths = {route.path for route in app.routes}
    assert "/health" in paths
    assert "/v1/twin/state" in paths
    assert "/v1/scenarios/run" in paths
    assert "/v1/capabilities" in paths
