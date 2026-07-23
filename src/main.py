import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
CONFIG_PATH = Path(__file__).parent.parent / "config" / "testnet.json"

def load_config():
    return json.loads(CONFIG_PATH.read_text())

CONFIG = load_config()

VALIDATORS = [
    {"id": "validator-alpha", "tolerance": 0.00},
    {"id": "validator-beta", "tolerance": 0.02},
    {"id": "validator-gamma", "tolerance": -0.02},
]


def validate_observation(obs, validator):
    temperature = float(obs["temperature_c"])
    humidity = float(obs["humidity_pct"])
    tolerance = validator["tolerance"]

    temp_ok = (-40 * (1 + tolerance)) <= temperature <= (85 * (1 + tolerance))
    humidity_ok = 0 <= humidity <= (100 * (1 + tolerance))

    return {
        "validator": validator["id"],
        "accepted": temp_ok and humidity_ok,
        "checks": {
            "temperature_range": temp_ok,
            "humidity_range": humidity_ok,
        },
    }


def verify(obs):
    votes = [
        validate_observation(obs, validator)
        for validator in VALIDATORS
    ]

    accepted_votes = sum(
        1 for vote in votes if vote["accepted"]
    )

    confidence = accepted_votes / len(votes)

    status = "VERIFIED" if confidence >= 2 / 3 else "REJECTED"

    receipt = {
        "sensor_id": obs["sensor_id"],
        "timestamp": obs["timestamp"],
        "workload": "environmental-sensor-validation",
        "validator_votes": votes,
        "confidence": round(confidence, 4),
        "status": status,
        "verified_at": datetime.now(timezone.utc).isoformat(),
    }

    canonical = json.dumps(
        receipt,
        sort_keys=True,
        separators=(",", ":"),
    )

    receipt["popw_receipt_hash"] = hashlib.sha256(
        canonical.encode()
    ).hexdigest()

    return receipt


def main():
    data_path = (
        Path(__file__).parent
        / "data"
        / "sample_sensor_data.json"
    )

    observations = json.loads(
        data_path.read_text()
    )
    results = []

    print("NexusAI Network - PoPW Sensor Verification Prototype")

    for obs in observations:
        result = verify(obs)
        results.append(result)

        print(f'\nSensor: {result["sensor_id"]}')

        for vote in result["validator_votes"]:
            decision = "ACCEPT" if vote["accepted"] else "REJECT"
            validator = vote["validator"]
            print(f"  {validator}: {decision}")

        print(f'Confidence: {result["confidence"]}')
        print(f'Status: {result["status"]}')
        print(f'PoPW Receipt: {result["popw_receipt_hash"]}')

    output_path = Path(__file__).parent / "demo_output.json"

    output = {
        "project": "NexusAI Network",
        "prototype": "PoPW Sensor Verification",
        "network": "Konnex",
        "results": results
    }

    output_path.write_text(
        json.dumps(output, indent=2)
    )

    print(f"\nDemo output saved to: {output_path}")


if __name__ == "__main__":
    main()
