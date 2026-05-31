#config.py
import os

DISASTER_THRESHOLD = 0.70
HELP_THRESHOLD = 0.60
TIME_WINDOW_HOURS = 6

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "c46d1ff1c1d64c769eb3db649e251994")

AUTHORITIES = {
    "food": "aarshanm4@gmail.com",
    "rescue": "rescue.team.alert@gmail.com",
    "medical": "krishnendumv76@gmail.com",
    "shelter": "project.alertingsystem@gmail.com",
    "emergency_resources": "disasterauthorities@gmail.com"
}

EMAIL_CONFIG = {
    "sender": os.getenv("EMAIL_SENDER", "disaster.rescue.alert@gmail.com"),
    "password": os.getenv("EMAIL_PASSWORD", "vrhw xupi zxmw knng")
}