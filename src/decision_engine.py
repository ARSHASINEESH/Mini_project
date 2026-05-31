# src/decision_engine.py
from src.config import DISASTER_THRESHOLD


def make_final_decision(disaster_prob, verification, rule_result):
    verification_confidence = verification.get("confidence", 0.0)
    verification_status = verification.get("status", "UNVERIFIED")
    rule_score = rule_result.get("score", 0.0)

    final_truth_score = (
        0.45 * disaster_prob +
        0.30 * verification_confidence +
        0.25 * rule_score
    )

    final_truth_score = round(final_truth_score, 2)

    if disaster_prob >= DISASTER_THRESHOLD and (
        verification_status == "VERIFIED" or rule_score > 0.75 or final_truth_score >= 0.70
    ):
        final_decision = "REAL"
    else:
        final_decision = "FAKE"

    return {
        "decision": final_decision,
        "final_truth_score": final_truth_score
    }