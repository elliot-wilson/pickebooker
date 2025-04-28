import argparse
import os
import plistlib
import subprocess
from datetime import datetime, timedelta

import pytz
from dotenv import load_dotenv

from extract_authentication_headers import extract_authentication_headers
from reserve import reserve

PLIST_DIR = f"{os.path.expanduser('~')}/Library/LaunchAgents/"


def main(
    date: str,
    time: str,
    court: int = 3,
    duration: int = 90,
) -> None:
    target_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    # bookings open 8 days in advance, so schedule the jobs for 8 days before the reservation date
    run_date = target_datetime - timedelta(days=8)

    booking_run_date = convert_to_local_equivalent_of_central(
        run_date, hour=9, minute=0
    )

    if booking_run_date < datetime.now():
        print(
            "👉 This timeslot has already been released, so I'll try to book it immediately"
        )
        extract_authentication_headers()
        reserve(
            date=date,
            time=time,
            court=court,
            duration=duration,
        )
        return

    auth_run_date = convert_to_local_equivalent_of_central(run_date, hour=8, minute=55)

    schedule_authentication_refresh(run_date=auth_run_date)
    schedule_court_booking_for_date(
        run_date=booking_run_date,
        reservation_date=date,
        reservation_time=time,
        court=court,
        duration=duration,
    )


def schedule_authentication_refresh(*, run_date: datetime) -> None:
    load_dotenv()
    label = f"com.picklebooker.refresh.{run_date.strftime('%Y-%m-%d')}"
    script_path = os.path.abspath("extract_authentication_headers.py")
    arguments = [
        os.getenv("PYTHON_PATH"),
        script_path,
    ]

    print("Scheduling authentication refresh job...")
    create_plist(label=label, arguments=arguments, run_date=run_date)


def schedule_court_booking_for_date(
    *,
    run_date: str,
    reservation_date,
    reservation_time: str,
    court: int = 3,
    duration: int = 90,
) -> None:
    load_dotenv()
    label = f"com.picklebooker.book.{run_date.strftime('%Y-%m-%d')}"

    script_path = os.path.abspath("reserve.py")
    arguments = [
        os.getenv("PYTHON_PATH"),
        script_path,
        "--date",
        reservation_date,
        "--time",
        reservation_time,
        "--court",
        str(court),
        "--duration",
        str(duration),
    ]

    print(
        f"Scheduling booking job for {duration} minutes at court {court} on {reservation_date} at {reservation_time}..."
    )
    create_plist(label=label, arguments=arguments, run_date=run_date)


def create_plist(label: str, arguments: list, run_date: datetime) -> None:
    plist_path = os.path.join(PLIST_DIR, f"{label}.plist")
    plist = {
        "Label": label,
        "ProgramArguments": arguments,
        "EnvironmentVariables": {"LAUNCH_AGENT_PATH": plist_path},
        "StartCalendarInterval": {
            "Year": run_date.year,
            "Month": run_date.month,
            "Day": run_date.day,
            "Hour": run_date.hour,
            "Minute": run_date.minute,
        },
        "StandardOutPath": f"/tmp/{label}.out",
        "StandardErrorPath": f"/tmp/{label}.err",
    }
    with open(plist_path, "wb") as f:
        plistlib.dump(plist, f)
    subprocess.run(["launchctl", "load", plist_path])
    print(
        f"✅ Scheduled job for {run_date.strftime('%Y-%m-%d %H:%M')}. You can inspect the plist at {plist_path}"
    )


def convert_to_local_equivalent_of_central(
    run_date: datetime, hour: int, minute: int = 0
) -> datetime:
    chicago_tz = pytz.timezone("America/Chicago")  # well, St. Louis, but close enough
    local_tz = datetime.now().astimezone().tzinfo

    central_target = chicago_tz.localize(
        datetime(run_date.year, run_date.month, run_date.day, hour, minute)
    )

    return central_target.astimezone(local_tz)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--date",
        required=True,
        type=str,
        help="Target date to book. Format: YYYY-MM-DD. Example: 2025-04-28",
    )
    parser.add_argument(
        "--time",
        type=str,
        required=True,
        help="Time to book. Format: HH:MM (24-hour format). Example: 14:30",
    )
    parser.add_argument(
        "--court",
        type=int,
        choices=[1, 2, 3],
        default=3,
        help="Court number. Default is 3.",
    )
    parser.add_argument(
        "--duration",
        type=int,
        choices=[30, 60, 90],
        default=90,
        required=False,
        help="Length of the booking. Default is 90 minutes.",
    )
    args = parser.parse_args()
    main(
        date=args.date,
        time=args.time,
        court=args.court,
        duration=args.duration,
    )
