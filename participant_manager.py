from config import PARTICIPANT_FILE
from storage import load_data, save_data, next_id
from utils import read_text, valid_email, print_table


def add_participant():
    participants = load_data(PARTICIPANT_FILE)

    print("\n--- Register Participant Profile ---")
    name = read_text("Full name: ")
    email = read_text("Email address: ").lower()

    if not valid_email(email):
        print("Enter a valid email address.")
        return

    phone = read_text("Phone number: ")

    if not phone.isdigit() or not 10 <= len(phone) <= 15:
        print("Phone number must contain 10 to 15 digits.")
        return

    if any(p["phone"] == phone for p in participants):
        print("This phone number is already registered.")
        return

    if any(p["email"].lower() == email for p in participants):
        print("This email address is already registered.")
        return

    participant = {
        "id": next_id(participants),
        "name": name,
        "email": email,
        "phone": phone
    }

    participants.append(participant)
    save_data(PARTICIPANT_FILE, participants)

    print(
        "Participant profile created. "
        f"Participant ID: {participant['id']}"
    )


def list_participants():
    participants = load_data(PARTICIPANT_FILE)

    print_table(
        ["ID", "Name", "Email", "Phone"],
        [
            [p["id"], p["name"], p["email"], p["phone"]]
            for p in participants
        ]
    )


def get_participant(participant_id):
    return next(
        (
            p for p in load_data(PARTICIPANT_FILE)
            if p["id"] == participant_id
        ),
        None
    )


def participant_menu():
    while True:
        print("\n--- Participant Management ---")
        print("1. Create participant profile")
        print("2. View participants")
        print("0. Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            add_participant()
        elif choice == "2":
            list_participants()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
