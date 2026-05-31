#notifier.py
import re
import smtplib
from email.mime.text import MIMEText
from src.config import AUTHORITIES, EMAIL_CONFIG


def extract_location(text):
    hashtags = re.findall(r"#([A-Za-z]+)", text)
    if hashtags:
        return hashtags[-1]

    location_patterns = [
        r"\bin\s([A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)*)",
        r"\bat\s([A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)*)",
        r"\bnear\s([A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)*)",
        r"\bfrom\s([A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)*)"
    ]

    for pattern in location_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)

    multi_word = re.findall(r"\b([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)\b", text)
    if multi_word:
        return multi_word[-1]

    return "Location not detected"


def extract_need(text):
    text = text.lower()
    detected_needs = set()

    if any(w in text for w in ["food", "water", "hungry", "ration", "meal", "drinking water"]):
        detected_needs.add("food")

    if any(w in text for w in ["rescue", "trapped", "evacuate", "stuck", "save us", "stranded"]):
        detected_needs.add("rescue")

    if any(w in text for w in ["medicine", "injured", "hospital", "ambulance", "medical", "doctor"]):
        detected_needs.add("medical")

    if any(w in text for w in ["shelter", "homeless", "camp", "stay", "accommodation"]):
        detected_needs.add("shelter")

    if any(w in text for w in [
        "clothes", "clothing", "pads", "diapers", "baby", "blanket",
        "supplies", "pharmacy", "sanitary", "steam machine", "essentials"
    ]):
        detected_needs.add("emergency_resources")

    return list(detected_needs)


def send_email(receiver, subject, body):
    if not EMAIL_CONFIG["sender"] or not EMAIL_CONFIG["password"]:
        print("❌ Email credentials are missing.")
        return False

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_CONFIG["sender"]
    msg["To"] = receiver

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_CONFIG["sender"], EMAIL_CONFIG["password"])
            server.send_message(msg)

        print(f"✅ Email sent successfully to {receiver}")
        return True

    except Exception as e:
        print("❌ Email failed:", e)
        return False


def notify_authority(text):
    needs = extract_need(text)

    if not needs:
        print("No specific Need identified.")
        return []

    location = extract_location(text)
    subject = "🚨 Disaster Help Request Detected"

    body = f"""
Disaster Alert Detected

Location: {location}

Needs Identified:
{', '.join(needs).upper()}

Message:
{text}

Please respond immediately.
"""

    email_logs = []

    for need in needs:
        email = AUTHORITIES.get(need)

        if not email:
            continue

        print(f"📧 Sending alert to {email} ({need})")
        success = send_email(email, subject, body)

        email_logs.append({
            "need": need,
            "email": email,
            "status": "success" if success else "failed"
        })

    return email_logs