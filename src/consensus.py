def calculate_consensus(votes, threshold=0.67):
    if not votes:
        return {
            "status": "REJECTED",
            "confidence": 0.0,
            "validator_count": 0
        }

    verified_votes = sum(
        1 for vote in votes
        if vote.get("status") == "VERIFIED"
    )

    total_votes = len(votes)
    confidence = verified_votes / total_votes

    status = (
        "VERIFIED"
        if confidence >= threshold
        else "REJECTED"
    )

    return {
        "status": status,
        "confidence": round(confidence, 4),
        "validator_count": total_votes
    }


if __name__ == "__main__":
    demo_votes = [
        {"validator": "validator-01", "status": "VERIFIED"},
        {"validator": "validator-02", "status": "VERIFIED"},
        {"validator": "validator-03", "status": "REJECTED"},
    ]

    result = calculate_consensus(demo_votes)

    print("NexusAI Multi-Validator Consensus")
    print(result)
