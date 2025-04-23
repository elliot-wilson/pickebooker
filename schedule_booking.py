import argparse
import os
import plistlib
import subprocess
import uuid
from datetime import datetime, timedelta


def schedule_run(target_date_str, start_gte, start_lte):
    target_date = datetime.strptime(target_date_str, "%Y-%m-%d")
    run_date = target_date - timedelta(days=8)

    label = f"com.picklebooker.{uuid.uuid4().hex[:8]}"
    plist_path = f"{os.path.expanduser('~')}/Library/LaunchAgents/{label}.plist"

    script_path = os.path.abspath("book_court.py")
    arguments = [
        "/Users/elliotwilson/work/picklebooker/.venv/bin/python",
        script_path,
        "--date",
        target_date_str,
        "--start-gte",
        str(start_gte),
        "--start-lte",
        str(start_lte),
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
    print(f"Scheduling at {run_date.strftime('%Y-%m-%d %H:%M')} (local time)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--target-date", required=True, help="Date to book (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--start-gte", type=int, required=True, help="Start hour (0-23)"
    )
    parser.add_argument("--start-lte", type=int, required=True, help="End hour (0-23)")
    args = parser.parse_args()

    schedule_run(args.target_date, args.start_gte, args.start_lte)
