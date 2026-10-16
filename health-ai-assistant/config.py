"""
Configuration and Application Settings
AI Healthcare Diagnosis Assistant
Architected by Shashank Dixit
"""

import os

APP_TITLE = "MediAI Pro — AI Healthcare Diagnosis Assistant"
APP_SUBTITLE = "Clinical Decision Support & Differential Triage Engine"
APP_VERSION = "2.5.0"
AUTHOR_NAME = "Shashank Dixit"
AUTHOR_TITLE = "Lead AI Systems Architect & Healthcare Developer"
PORT = int(os.environ.get("PORT", 8000))
HOST = os.environ.get("HOST", "127.0.0.1")

# Emergency helpline numbers
EMERGENCY_HOTLINES = [
    {"name": "National Emergency (Universal)", "number": "112", "desc": "Police, Fire, Ambulance"},
    {"name": "Emergency Medical / Ambulance", "number": "108", "desc": "Direct Medical Ambulance Helpline"},
    {"name": "National Health Helpline", "number": "1800-180-1104", "desc": "Toll-free tele-consultation"},
    {"name": "Poison Control Center", "number": "1800-116-117", "desc": "Toxicology and poison emergency"},
    {"name": "Mental Health Support (Tele-MANAS)", "number": "14416", "desc": "24/7 psychological assistance"}
]
