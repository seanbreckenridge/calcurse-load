import sys
import os
import argparse
from datetime import date

from gcsa.google_calendar import GoogleCalendar

default_credential_file = os.path.join(os.environ["HOME"], ".credentials", "google_calendar_credentials.json")


def create_calendar(email: str,
                    credential_file: str) -> GoogleCalendar:
    return GoogleCalendar(email, credential_file)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Export Google Calendar events"
    )
    required = parser.add_argument_group("required options")
    parser.add_argument("--email", help="Google Email to export", required=True)
    parser.add_argument("--credential-file", help="Google credential file", default=default_credential_file)
    export_to = parser.add_argument_group("export to...")
    export_choice = export_to.add_mutually_exclusive_group(required=True)
    export_choice.add_argument(
        "--csv",
        help="Export calendar events to a CSV file",
    )
    export_choice.add_argument(
        "--ics",
        help="Export calendar events to an ICS file",
    )
    return parser.parse_args()

def main():
    args = parse_args()
    if not os.path.exists(args.credential_file):
        print(f"Credential file at {args.credential_file} doesn't exist...")
        sys.exit(1)
    cal = create_calendar(args.email, args.credential_file)
    events = []
    for event in cal.get_events(date(1900, 1, 1), date(2100, 1, 1)):
        events.append(event)
        print(event)
    return events


if __name__ == "__main__":
    main()
