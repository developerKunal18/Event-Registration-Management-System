
# Event Registration Management System

## Overview

A command-line application built with Python to manage events, participant profiles, event registrations, payments, and reports. The application stores information in JSON files.

## Features

- Create and view events
- Register participant profiles
- Register participants for events
- Prevent duplicate active registrations
- Enforce event capacity limits
- Cancel unpaid registrations
- Record registration payments
- View event-wise participant lists
- Track pending payments and collected revenue
- Generate monthly revenue reports

## Technologies Used

- Python 3.10+
- JSON
- Python standard library

## Installation

1. Install Python 3.10 or later.
2. Download or clone this repository.
3. Open a terminal in the project directory.
4. Run the application:

   ```bash
   python main.py
   ```

No external packages are required.

## Project Structure

```text
day356_event_registration/
├── main.py
├── config.py
├── storage.py
├── utils.py
├── event_manager.py
├── participant_manager.py
├── registration_manager.py
├── payment_manager.py
├── report_manager.py
├── requirements.txt
├── .gitignore
├── README.md
└── data/
    ├── events.json
    ├── participants.json
    ├── registrations.json
    └── payments.json
```

## How to Use

1. Create an event with a name, category, date, venue, capacity, and fee.
2. Create a participant profile.
3. Register the participant using the participant ID and event ID.
4. Record payment using the generated registration ID.
5. View the participant list and event reports.
6. Check the dashboard for revenue and outstanding payments.

## Testing Checklist

- Create an event with a future date.
- Create a participant profile.
- Register the participant for an event.
- Attempt to register the same participant again.
- Attempt to exceed event capacity.
- Record a payment and try to record it again.
- Cancel an unpaid registration.
- Check the event report and monthly revenue report.

## Storage

Records are stored in the `data` directory as JSON files. Back up this directory regularly.

## Limitations

- This is a local learning project, not a production ticketing platform.
- JSON files are not suitable for concurrent multi-user access.
- Payments are recorded manually; no payment gateway is connected.
- Automatic refunds are not supported.
- Login, authentication, and role-based permissions are not included.

## Future Improvements

- Add a graphical interface using Tkinter.
- Add event search and CSV export.
- Add QR-code tickets.
- Add email confirmation.
- Connect MySQL or SQLite.
- Add automated tests with `unittest`.
