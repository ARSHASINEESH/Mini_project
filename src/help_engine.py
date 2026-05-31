#help_engine.py
from src.classifier import predict_help


HELP_KEYWORDS = {
    "rescue": [
        "rescue", "rescued", "seeking rescue", "emergency rescue",
        "need rescue", "waiting to be rescued", "waiting for rescue",
        "trapped", "stranded", "save us", "evacuate", "evacuation",
        "people trapped", "stuck"
    ],
    "food": [
        "food", "water", "hungry", "ration", "meal", "drinking water"
    ],
    "medical": [
        "medicine", "medical", "doctor", "ambulance", "injured",
        "hospital", "treatment"
    ],
    "shelter": [
        "shelter", "camp", "homeless", "accommodation", "stay"
    ],
    "emergency_resources": [
        "clothes", "clothing", "pads", "diapers", "blanket", "baby",
        "sanitary", "essentials", "supplies", "pharmacy"
    ]
}

GENERAL_HELP_PHRASES = [
    "need help",
    "needs help",
    "any help",
    "help possible",
    "please help",
    "help needed",
    "urgent help",
    "need support",
    "seeking help",
    "seeking rescue",
    "seeking emergency rescue",
    "asking for help",
    "requesting help",
    "requesting rescue",
    "people seeking",
    "people are seeking"
]


def keyword_help_score(text):
    text_lower = text.lower()
    score = 0.0
    matched = []

    for phrase in GENERAL_HELP_PHRASES:
        if phrase in text_lower:
            score += 0.20
            matched.append(phrase)

    for category, words in HELP_KEYWORDS.items():
        for word in words:
            if word in text_lower:
                score += 0.12
                matched.append(word)

    score = min(score, 1.0)
    return round(score, 2), matched


def detect_help(text):
    ml_prob = predict_help(text)
    rule_score, matched_keywords = keyword_help_score(text)

    final_help_score = round((0.4 * ml_prob) + (0.6 * rule_score), 2)

    is_help = final_help_score >= 0.35

    return {
        "ml_help_probability": round(ml_prob, 2),
        "rule_help_score": rule_score,
        "final_help_probability": final_help_score,
        "is_help": is_help,
        "matched_help_keywords": matched_keywords
    }