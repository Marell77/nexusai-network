import hashlib
import json
import sys
from pathlib import Path


OUTPUT_PATH = Path(__file__).parent / "demo_output.json"


def fail(message):
    print(f"FAIL: {message}")
    sys.exit(1)


def main():
    if not OUTPUT_PATH.exists():
        fail("demo_output.json not found")

    try:
        data = json.loads(OUTPUT_PATH.read_text())
    except json.JSONDecodeError as exc:
        fail(f"Invalid JSON: {exc}")

    required = [
        "project",
        "environment",
        "network",
        "prototype",
        "results",
    ]

    for field in required:
        if field not in data:
            fail(f"Missing field: {field}")

    prototype = data["prototype"]

    for field in [
        "type",
        "validator_count",
        "consensus_threshold",
    ]:
        if field not in prototype:
            fail(f"Missing prototype field: {field}")

    results = data["results"]

    if not isinstance(results, list) or not results:
        fail("No verification results found")

            for index, result in enumerate(results):
        required_result_fields = [
            "sensor_id",
            "validator_votes",
            "confidence",
            "status",
            "popw_receipt_hash",
        ]

        for field in required_result_fields:
            if field not in result:
                fail(f"Result {index} missing field: {field}")

        if result["status"] not in ("VERIFIED", "REJECTED"):
            fail(f"Result {index} has invalid status")

        receipt_hash = result["popw_receipt_hash"]

        if not isinstance(receipt_hash, str) or len(receipt_hash) != 64:
            fail(f"Result {index} has invalid SHA-256 hash")

        receipt_without_hash = {
            key: value
            for key, value in result.items()
            if key != "popw_receipt_hash"
        }

        canonical = json.dumps(
            receipt_without_hash,
            sort_keys=True,
            separators=(",", ":"),
        )

        calculated_hash = hashlib.sha256(
            canonical.encode()
        ).hexdigest()

        if calculated_hash != receipt_hash:
            fail(f"Result {index} PoPW receipt hash mismatch")

    print("PoPW receipt validation PASSED")
    print(f"Project: {data['project']}")
    print(f"Network: {data['network']}")
    print(f"Results verified: {len(results)}")



        if __name__ == "__main__":
        main()
