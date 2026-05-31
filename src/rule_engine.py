# src/rule_engine.py
import re


DISASTER_HASHTAGS = {
    "flood", "floods", "earthquake", "cyclone", "storm", "landslide",
    "fire", "wildfire", "tsunami", "rescue", "emergency", "disaster",
    "evacuation", "rain", "heavyrain", "covid", "pandemic"
}

SENSATIONAL_WORDS = [
    "breaking", "share please", "please share", "viral", "must watch",
    "shocking", "unbelievable"
]

VAGUE_WORDS = [
    "something happened", "something terrible", "somewhere", "maybe",
    "not sure", "i think", "probably", "seems like", "kind of"
]

FIRST_PERSON_PATTERNS = [
    r"\bi felt\b",
    r"\bmy building\b",
    r"\bmy house\b",
    r"\bi saw\b",
    r"\bwe are trapped\b",
    r"\bi am trapped\b",
    r"\bour area\b"
]

DISASTER_WORDS = [
    "earthquake", "flood", "cyclone", "storm", "landslide",
    "fire", "explosion", "accident", "tsunami", "covid", "pandemic"
]


def _clamp(value, low=0.0, high=1.0):
    return max(low, min(high, value))


def _has_event_location_time(text):
    text_lower = text.lower()

    has_event = any(word in text_lower for word in DISASTER_WORDS)

    has_location = bool(re.search(r"\b(in|at|near|from)\s+[A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)*", text)) \
        or bool(re.search(r"#([A-Za-z]+)", text)) \
        or bool(re.search(r"\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)+\b", text))

    has_time = bool(re.search(r"\b\d{1,2}[./-]\d{1,2}[./-]\d{2,4}\b", text)) \
        or bool(re.search(r"\b(today|yesterday|tonight|this morning|this evening|now)\b", text_lower)) \
        or bool(re.search(r"\b\d{1,2}:\d{2}\b", text))

    return has_event and has_location and has_time


def _too_many_emojis(text):
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "]+",
        flags=re.UNICODE
    )
    emojis = emoji_pattern.findall(text)
    emoji_count = sum(len(item) for item in emojis)
    return emoji_count >= 4


def _has_sensational_words(text):
    text_lower = text.lower()
    return any(word in text_lower for word in SENSATIONAL_WORDS)


def _too_many_special_characters(text):
    count = len(re.findall(r"[!@#$%^&*_=+~`|<>/\\]", text))
    return count >= 6


def _is_question_format(text):
    text_lower = text.lower().strip()
    return "?" in text or text_lower.startswith((
        "is ", "are ", "can ", "did ", "does ", "what ", "when ", "where ", "why ", "how "
    ))


def _has_first_person_witness(text):
    text_lower = text.lower()
    return any(re.search(pattern, text_lower) for pattern in FIRST_PERSON_PATTERNS)


def _has_vague_language(text):
    text_lower = text.lower()
    return any(word in text_lower for word in VAGUE_WORDS)


def _has_numeric_specificity(text):
    return bool(re.search(r"\b\d+\b", text))


def _too_many_caps(text):
    words = re.findall(r"\b[A-Z]{3,}\b", text)
    return len(words) >= 3


def _has_url(text):
    return bool(re.search(r"https?://|www\.", text.lower()))


def _is_too_short(text):
    return len(text.split()) < 5


def _too_many_hashtags(text):
    hashtags = re.findall(r"#\w+", text)
    return len(hashtags) >= 4


def _has_non_disaster_hashtags(text):
    hashtags = [tag.lower().replace("#", "") for tag in re.findall(r"#\w+", text)]
    if not hashtags:
        return False
    non_disaster = [tag for tag in hashtags if tag not in DISASTER_HASHTAGS]
    return len(non_disaster) >= 2


def evaluate_credibility(text):
    score = 0.50
    applied_rules = []

    # Positive rules
    if _has_event_location_time(text):
        score += 0.18
        applied_rules.append(("event_location_time", "+0.18"))

    if _has_first_person_witness(text):
        score += 0.14
        applied_rules.append(("first_person_witness", "+0.14"))

    if _has_numeric_specificity(text):
        score += 0.10
        applied_rules.append(("numeric_specificity", "+0.10"))

    # Small positive if disaster word exists at all
    if any(word in text.lower() for word in DISASTER_WORDS):
        score += 0.08
        applied_rules.append(("disaster_keyword_present", "+0.08"))

    # Negative rules
    if _too_many_emojis(text):
        score -= 0.08
        applied_rules.append(("too_many_emojis", "-0.08"))

    if _has_sensational_words(text):
        score -= 0.12
        applied_rules.append(("sensational_words", "-0.12"))

    if _too_many_special_characters(text):
        score -= 0.08
        applied_rules.append(("too_many_special_characters", "-0.08"))

    if _is_question_format(text):
        score -= 0.07
        applied_rules.append(("question_format", "-0.07"))

    if _has_vague_language(text):
        score -= 0.10
        applied_rules.append(("vague_language", "-0.10"))

    if _too_many_caps(text):
        score -= 0.08
        applied_rules.append(("too_many_caps", "-0.08"))

    if _has_url(text):
        score -= 0.05
        applied_rules.append(("url_presence", "-0.05"))

    if _is_too_short(text):
        score -= 0.08
        applied_rules.append(("extremely_short", "-0.08"))

    if _too_many_hashtags(text):
        score -= 0.06
        applied_rules.append(("too_many_hashtags", "-0.06"))

    if _has_non_disaster_hashtags(text):
        score -= 0.08
        applied_rules.append(("non_disaster_hashtags", "-0.08"))

    score = _clamp(score)

    if score > 0.75:
        label = "High Credibility"
    elif score >= 0.40:
        label = "Unverified"
    else:
        label = "Low Credibility"

    return {
        "score": round(score, 2),
        "label": label,
        "applied_rules": applied_rules
    }