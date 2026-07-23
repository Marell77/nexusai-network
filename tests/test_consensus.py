import json
import subprocess
import sys
from pathlib import Path


def test_consensus_prototype_runs():
    result = subprocess.run(
        [sys.executable, "src/main.py"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0


def test_demo_output_contains_results():
    subprocess.run(
        [sys.executable, "src/main.py"],
        check=True
    )

    output_path = Path("src/demo_output.json")

    assert output_path.exists()

    data = json.loads(output_path.read_text())

    assert "results" in data
    assert len(data["results"]) > 0


def test_consensus_metadata():
    subprocess.run(
        [sys.executable, "src/main.py"],
        check=True
    )

    data = json.loads(Path("src/demo_output.json").read_text())

    for result in data["results"]:
        assert "status" in result
        assert result["status"] in ("VERIFIED", "REJECTED")
        assert "confidence" in result
        assert "consensus_validator_count" in result
        assert "popw_receipt_hash" in result
        assert len(result["popw_receipt_hash"]) == 64
