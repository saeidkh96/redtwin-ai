from redtwin.events import EventStore, capability_document


def test_capability_contract_is_versioned() -> None:
    document = capability_document()
    assert document["protocol"] == "rednexus_capability_v1"
    assert any(item["name"] == "redtwin.scenario.run" for item in document["capabilities"])


def test_event_envelope_has_cloudevents_fields() -> None:
    event = EventStore().publish("redtwin.tick.completed", {"tick": 1})
    assert event["specversion"] == "1.0"
    assert event["source"] == "redtwin-ai"
