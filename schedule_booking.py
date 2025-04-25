import argparse
import os
import plistlib
import subprocess
import uuid
from datetime import datetime, timedelta


def schedule_run(
    target_date: str, target_time: str, court: int = 3, duration: int = 90
) -> None:
    target_datetime = datetime.strptime(
        f"{target_date} {target_time}", "%Y-%m-%d %H:%M"
    )
    run_date = target_datetime - timedelta(days=8)

    # create plist for refreshing authentication headers
    label = f"com.picklebooker.refresh.{uuid.uuid4().hex[:8]}"
    plist_path = f"{os.path.expanduser('~')}/Library/LaunchAgents/{label}.plist"
    script_path = os.path.abspath("extract_authentication_headers.py")

    arguments = [
        "/Users/elliotwilson/work/picklebooker/.venv/bin/python",
        script_path,
    ]
    plist = {
        "Label": label,
        "ProgramArguments": arguments,
        "EnvironmentVariables": {"LAUNCH_AGENT_PATH": plist_path},
        "StartCalendarInterval": {
            "Year": run_date.year,
            "Month": run_date.month,
            "Day": run_date.day,
            "Hour": 8,
            "Minute": 55,
        },
        "StandardOutPath": f"/tmp/{label}.out",
        "StandardErrorPath": f"/tmp/{label}.err",
        "RunAtLoad": True,
    }
    with open(plist_path, "wb") as f:
        plistlib.dump(plist, f)
    subprocess.run(["launchctl", "load", plist_path])
    print(f"Scheduled authentication refresh for {target_date} at 8:55 AM.")
    print(f"You can inspect the plist at {plist_path}")

    # create plist for making booking
    label = f"com.picklebooker.{uuid.uuid4().hex[:8]}"
    plist_path = f"{os.path.expanduser('~')}/Library/LaunchAgents/{label}.plist"

    script_path = os.path.abspath("reserve.py")
    arguments = [
        "/Users/elliotwilson/work/picklebooker/.venv/bin/python",
        script_path,
        "--date",
        target_date,
        "--time",
        target_time,
        "--court",
        court,
        "--duration",
        duration,
    ]

    plist = {
        "Label": label,
        "ProgramArguments": arguments,
        "EnvironmentVariables": {"LAUNCH_AGENT_PATH": plist_path},
        "StartCalendarInterval": {
            "Year": run_date.year,
            "Month": run_date.month,
            "Day": run_date.day,
            "Hour": 9,
            "Minute": 0,
        },
        "StandardOutPath": f"/tmp/{label}.out",
        "StandardErrorPath": f"/tmp/{label}.err",
        "RunAtLoad": True,
    }

    with open(plist_path, "wb") as f:
        plistlib.dump(plist, f)

    subprocess.run(["launchctl", "load", plist_path])
    print(
        f"Scheduled booking job for {duration} minutes at court {court} on {target_date} at {target_time}."
    )
    print(f"The job is scheduled for {run_date.strftime('%Y-%m-%d %H:%M')}.")
    print(f"You can inspect the plist at {plist_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--target-date",
        required=True,
        type=str,
        help="Date to book. Format: YYYY-MM-DD. Example: 2025-04-28",
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
    schedule_run(
        target_date=args.target_date,
        target_time=args.time,
        court=args.court,
        duration=args.duration,
    )
