from datetime import date

from config import EVENT_FILE, REGISTRATION_FILE, PAYMENT_FILE
from storage import load_data, save_data, next_id
from event_manager import get_event
from participant_manager import get_participant
from utils import (
    read_positive_int,
    print_table,
    timestamp
)


def register_for_event():
    print("\n--- Event Registration ---")

    participant_id = read_positive_int("Participant ID: ")
    participant = get_participant(participant_id)

    if not participant:
        print("Participant not found. Create a profile first.")
        return

    event_id = read_positive_int("Event ID: ")
    event = get_event(event_id)

    if not event:
        print("Event not found.")
        return

    if event["status"] != "Open":
        print("This event is not open for registration.")
        return

    if date.fromisoformat(event["date"]) < date.today():
        print("Registration is closed because the event date has passed.")
        return

    registrations = load_data(REGISTRATION_FILE)

    duplicate = any(
        r["participant_id"] == participant_id
        and r["event_id"] == event_id
        and r["status"] == "Confirmed"
        for r in registrations
    )

    if duplicate:
        print("This participant is already registered for the event.")
        return

    confirmed_count = sum(
        r["event_id"] == event_id and r["status"] == "Confirmed"
        for r in registrations
    )

    if confirmed_count >= event["capacity"]:
        print("This event has reached its maximum capacity.")
        return

    registration = {
        "id": next_id(registrations),
        "participant_id": participant_id,
        "event_id": event_id,
        "fee": float(event["fee"]),
        "status": "Confirmed",
        "created_at": timestamp()
    }

    registrations.append(registration)
    save_data(REGISTRATION_FILE, registrations)

    print("Registration successful.")
    print(f"Registration ID: {registration['id']}")
    print(f"Event: {event['name']}")
    print(f"Registration fee: ₹{event['fee']:.2f}")
    print("Payment status: Pending")


def list_registrations():
    registrations = load_data(REGISTRATION_FILE)

    participants = {
        p["id"]: p["name"]
        for p in load_data("data/participants.json")
    }

    events = {
        e["id"]: e["name"]
        for e in load_data(EVENT_FILE)
    }

    print_table(
        ["Registration ID", "Participant", "Event", "Fee", "Status"],
        [
            [
                r["id"],
                participants.get(r["participant_id"], "Unknown"),
                events.get(r["event_id"], "Unknown"),
                f"₹{r['fee']:.2f}",
                r["status"]
            ]
            for r in registrations
        ]
    )


def cancel_registration():
    print("\n--- Cancel Registration ---")

    registration_id = read_positive_int("Registration ID: ")
    registrations = load_data(REGISTRATION_FILE)

    registration = next(
        (
            r for r in registrations
            if r["id"] == registration_id
            and r["status"] == "Confirmed"
        ),
        None
    )

    if not registration:
        print("Confirmed registration not found.")
        return

    payments = load_data(PAYMENT_FILE)

    if any(
        p["registration_id"] == registration_id
        and p["status"] == "Paid"
        for p in payments
    ):
        print(
            "This registration has a recorded payment. "
            "Handle the refund before cancellation; "
            "automatic refunds are not supported."
        )
        return

    registration["status"] = "Cancelled"
    registration["cancelled_at"] = timestamp()
    save_data(REGISTRATION_FILE, registrations)

    print("Registration cancelled successfully.")


def registration_menu():
    while True:
        print("\n--- Registration Management ---")
        print("1. Register for an event")
        print("2. View registrations")
        print("3. Cancel registration")
        print("0. Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            register_for_event()
        elif choice == "2":
            list_registrations()
        elif choice == "3":
            cancel_registration()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
