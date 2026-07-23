import hashlib
import hmac
import json


def create_validator_signature(validator_id, decision, secret):
    payload = {
        "validator_id": validator_id,
        "decision": decision,
    }

    canonical = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
    )

    signature = hmac.new(
        secret.encode(),
        canonical.encode(),
        hashlib.sha256,
    ).hexdigest()

    return signature


def verify_validator_signature(
    validator_id,
    decision,
    secret,
    signature,
):
    expected = create_validator_signature(
        validator_id,
        decision,
        secret,
    )

    return hmac.compare_digest(expected, signature)


if __name__ == "__main__":
    validator_id = "validator-001"
    decision = "ACCEPT"
    secret = "nexusai-test-validator-key"

    signature = create_validator_signature(
        validator_id,
        decision,
        secret,
    )

    print("NexusAI Validator Signature Test")
    print(f"Validator: {validator_id}")
    print(f"Decision: {decision}")
    print(f"Signature: {signature}")

    valid = verify_validator_signature(
        validator_id,
        decision,
        secret,
        signature,
    )

    if not valid:
        raise SystemExit("Validator signature verification FAILED")

    print("Validator signature verification PASSED")
