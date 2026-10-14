from config import PAYMENT_FILE, REGISTRATION_FILE, PAYMENT_METHODS
from storage import load_data, save_data, next_id
from utils import read_positive_int, print_table, timestamp, money


def record_payment():
    print("\n--- Record Event Payment ---")

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
        print("Payment has already been recorded.")
        return

    amount = float(registration["fee"])
    print(f"Amount due: {money(amount)}")
    print("Payment methods:", ", ".join(PAYMENT_METHODS))

    method = input("Payment method: ").strip().title()

    if method not in PAYMENT_METHODS:
        print("Invalid payment method.")
        return

    reference = input("Transaction reference (optional): ").strip()

    payment = {
        "id": next_id(payments),
        "registration_id": registration_id,
        "amount": round(amount, 2),
        "method": method,
        "reference": reference,
        "status": "Paid",
        "paid_at": timestamp()
    }

    payments.append(payment)
    save_data(PAYMENT_FILE, payments)

    print("Payment recorded successfully.")
    print(f"Receipt ID: {payment['id']}")
    print(f"Amount: {money(amount)}")


def list_payments():
    payments = load_data(PAYMENT_FILE)

    print_table(
        ["Payment ID", "Registration ID", "Amount",
         "Method", "Status", "Date"],
        [
            [
                p["id"],
                p["registration_id"],
                money(p["amount"]),
                p["method"],
                p["status"],
                p["paid_at"]
            ]
            for p in payments
        ]
    )


def payment_menu():
    while True:
        print("\n--- Payment Management ---")
        print("1. Record payment")
        print("2. View payment history")
        print("0. Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            record_payment()
        elif choice == "2":
            list_payments()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
