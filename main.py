from config import (
    EVENT_FILE,
    PARTICIPANT_FILE,
    REGISTRATION_FILE,
    PAYMENT_FILE
)
from storage import ensure_file

from event_manager import event_menu
from participant_manager import participant_menu
from registration_manager import registration_menu
from payment_manager import payment_menu
from report_manager import report_menu


def initialize():
    for file_path in [
        EVENT_FILE,
        PARTICIPANT_FILE,
        REGISTRATION_FILE,
        PAYMENT_FILE
    ]:
        ensure_file(file_path)


def main():
    initialize()

    while True:
        print("\n====================================")
        print("   EVENT REGISTRATION MANAGEMENT")
        print("====================================")
        print("1. Event management")
        print("2. Participant management")
        print("3. Registration management")
        print("4. Payment management")
        print("5. Reports")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                event_menu()
            elif choice == "2":
                participant_menu()
            elif choice == "3":
                registration_menu()
            elif choice == "4":
                payment_menu()
            elif choice == "5":
                report_menu()
            elif choice == "0":
                print("Thank you for using Event Registration Management.")
                break
            else:
                print("Invalid choice. Try again.")

        except (OSError, ValueError, KeyError) as error:
            print(f"Operation failed: {error}")
            print("Check the input and data files before retrying.")


if __name__ == "__main__":
    main()
