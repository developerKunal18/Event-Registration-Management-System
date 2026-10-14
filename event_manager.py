from datetime import date

from config import EVENT_FILE, EVENT_CATEGORIES
from storage import load_data, save_data, next_id
from utils import (
    read_text,
    read_positive_int,
    read_non_negative_float,
    read_date,
    print_table
)


def add_event():
    events = load_data(EVENT_FILE)

    print("\n--- Create Event ---")
    name = read_text("Event name: ")
    print("Categories:", ", ".join(EVENT_CATEGORIES))
    category = read_text("Category: ").title()

    if category not in EVENT_CATEGORIES:
        print("Invalid category.")
        return

    event_date = read_date("Event date (YYYY-MM-DD): ")

    if event_date < date.today():
        print("An event cannot be created for a past date.")
        return

    venue = read_text("Venue: ")
    capacity = read_positive_int("Maximum participants: ")
    fee = read_non_negative_float("Registration fee (₹): ")

    event = {
        "id": next_id(events),
        "name": name,
        "category": category,
        "date": event_date.isoformat(),
        "venue": venue,
        "capacity": capacity,
        "fee": fee,
        "status": "Open"
    }

    events.append(event)
    save_data(EVENT_FILE, events)

    print(f"Event created successfully. Event ID: {event['id']}")


def list_events():
    events = load_data(EVENT_FILE)

    print_table(
        ["ID", "Event", "Category", "Date", "Venue",
         "Capacity", "Fee", "Status"],
        [
            [
                e["id"], e["name"], e["category"], e["date"],
                e["venue"], e["capacity"], f"₹{e['fee']:.2f}",
                e["status"]
            ]
            for e in events
        ]
    )


def get_event(event_id):
    return next(
        (e for e in load_data(EVENT_FILE) if e["id"] == event_id),
        None
    )


def change_event_status(event_id, status):
    events = load_data(EVENT_FILE)

    for event in events:
        if event["id"] == event_id:
            event["status"] = status
            save_data(EVENT_FILE, events)
            return True

    return False


def event_menu():
    while True:
        print("\n--- Event Management ---")
        print("1. Create event")
        print("2. View events")
        print("0. Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            add_event()
        elif choice == "2":
            list_events()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
