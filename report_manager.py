from datetime import date

from config import (
    EVENT_FILE,
    PARTICIPANT_FILE,
    REGISTRATION_FILE,
    PAYMENT_FILE
)
from storage import load_data
from utils import print_table, money


def dashboard():
    events = load_data(EVENT_FILE)
    participants = load_data(PARTICIPANT_FILE)
    registrations = load_data(REGISTRATION_FILE)
    payments = load_data(PAYMENT_FILE)

    paid_revenue = sum(
        float(p["amount"])
        for p in payments
        if p["status"] == "Paid"
    )

    pending_amount = sum(
        float(r["fee"])
        for r in registrations
        if r["status"] == "Confirmed"
        and not any(
            p["registration_id"] == r["id"]
            and p["status"] == "Paid"
            for p in payments
        )
    )

    print("\n========== EVENT DASHBOARD ==========")
    print(f"Total events:            {len(events)}")
    print(f"Total participant profiles: {len(participants)}")
    print(
        "Confirmed registrations: "
        f"{sum(r['status'] == 'Confirmed' for r in registrations)}"
    )
    print(
        "Cancelled registrations: "
        f"{sum(r['status'] == 'Cancelled' for r in registrations)}"
    )
    print(f"Payments received:       {money(paid_revenue)}")
    print(f"Pending payment amount:  {money(pending_amount)}")
    print("=====================================")


def event_registration_report():
    events = load_data(EVENT_FILE)
    registrations = load_data(REGISTRATION_FILE)
    participants = {
        p["id"]: p["name"]
        for p in load_data(PARTICIPANT_FILE)
    }

    rows = []

    for event in events:
        event_registrations = [
            r for r in registrations
            if r["event_id"] == event["id"]
            and r["status"] == "Confirmed"
        ]

        rows.append([
            event["id"],
            event["name"],
            event["date"],
            event["capacity"],
            len(event_registrations),
            max(0, event["capacity"] - len(event_registrations)),
            event["status"]
        ])

    print_table(
        [
            "Event ID", "Event", "Date", "Capacity",
            "Registered", "Available Seats", "Status"
        ],
        rows
    )

    event_id_text = input(
        "\nEnter an event ID to see its participants, "
        "or press Enter to return: "
    ).strip()

    if not event_id_text:
        return

    try:
        event_id = int(event_id_text)
    except ValueError:
        print("Invalid event ID.")
        return

    selected_event = next(
        (e for e in events if e["id"] == event_id),
        None
    )

    if not selected_event:
        print("Event not found.")
        return

    selected_registrations = [
        r for r in registrations
        if r["event_id"] == event_id
        and r["status"] == "Confirmed"
    ]

    print(f"\nParticipants for: {selected_event['name']}")

    print_table(
        ["Registration ID", "Participant", "Fee", "Payment"],
        [
            [
                r["id"],
                participants.get(r["participant_id"], "Unknown"),
                money(r["fee"]),
                (
                    "Paid"
                    if any(
                        p["registration_id"] == r["id"]
                        and p["status"] == "Paid"
                        for p in load_data(PAYMENT_FILE)
                    )
                    else "Pending"
                )
            ]
            for r in selected_registrations
        ]
    )


def monthly_revenue_report():
    payments = load_data(PAYMENT_FILE)
    month = input("Enter month (YYYY-MM): ").strip()

    try:
        date.fromisoformat(month + "-01")
    except ValueError:
        print("Invalid month. Use YYYY-MM.")
        return

    monthly = [
        p for p in payments
        if p["status"] == "Paid"
        and p["paid_at"][:7] == month
    ]

    total = sum(float(p["amount"]) for p in monthly)

    print(f"\nRevenue for {month}: {money(total)}")
    print(f"Number of payments: {len(monthly)}")


def report_menu():
    while True:
        print("\n--- Reports ---")
        print("1. Business dashboard")
        print("2. Event registration report")
        print("3. Monthly revenue report")
        print("0. Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            dashboard()
        elif choice == "2":
            event_registration_report()
        elif choice == "3":
            monthly_revenue_report()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
