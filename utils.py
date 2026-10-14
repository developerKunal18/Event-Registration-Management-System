import re
from datetime import date, datetime


def read_text(prompt):
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("This field is required.")


def read_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt).strip())

            if value > 0:
                return value

            print("Enter a number greater than zero.")

        except ValueError:
            print("Enter a valid whole number.")


def read_non_negative_float(prompt):
    while True:
        try:
            value = float(input(prompt).strip())

            if value >= 0:
                return round(value, 2)

            print("Enter zero or a positive amount.")

        except ValueError:
            print("Enter a valid amount.")


def read_date(prompt):
    while True:
        value = input(prompt).strip()

        try:
            return date.fromisoformat(value)

        except ValueError:
            print("Use YYYY-MM-DD format, such as 2026-11-20.")


def valid_email(email):
    return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email))


def timestamp():
    return datetime.now().isoformat(timespec="seconds")


def money(amount):
    return f"₹{float(amount):,.2f}"


def print_table(headers, rows):
    if not rows:
        print("No records found.")
        return

    rows = [[str(value) for value in row] for row in rows]

    widths = [
        max(len(str(headers[i])), *(len(row[i]) for row in rows))
        for i in range(len(headers))
    ]

    print(" | ".join(
        str(headers[i]).ljust(widths[i])
        for i in range(len(headers))
    ))

    print("-+-".join("-" * width for width in widths))

    for row in rows:
        print(" | ".join(
            row[i].ljust(widths[i])
            for i in range(len(headers))
        ))
