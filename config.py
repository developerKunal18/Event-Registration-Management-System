from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

EVENT_FILE = DATA_DIR / "events.json"
PARTICIPANT_FILE = DATA_DIR / "participants.json"
REGISTRATION_FILE = DATA_DIR / "registrations.json"
PAYMENT_FILE = DATA_DIR / "payments.json"

EVENT_CATEGORIES = [
    "Workshop",
    "Seminar",
    "Conference",
    "Competition",
    "Cultural",
    "Sports",
    "Other"
]

PAYMENT_METHODS = ["Cash", "UPI", "Card", "Bank Transfer"]
