from src.consensus import verify


def test_valid_sensor_is_verified():
    observation = {
        "sensor_id": "test-sensor-001",
        "timestamp": "2026-07-23T00:00:00Z",
        "temperature_c": 25,
        "humidity": 60
    }

    result = verify(observation)

    assert result["status"] == "VERIFIED"
    assert result["confidence"] >= 0.6667
    assert result["consensus_validator_count"] == 3


def test_invalid_sensor_is_rejected():
    observation = {
        "sensor_id": "test-sensor-002",
        "timestamp": "2026-07-23T00:00:00Z",
        "temperature_c": 100,
        "humidity": 60
    }

    result = verify(observation)

    assert result["status"] == "REJECTED"
