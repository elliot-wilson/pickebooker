import argparse
import json
from datetime import datetime

import pytz
import requests

COURT_IDS = {
    1: "ZXhlcnA6MjgwYnI0ODAxOjcwMTU5MTE0MTUwOA==",
    2: "ZXhlcnA6MjgwYnI1MDAxOjcwMTU5MTE0MTUwOA==",
    3: "ZXhlcnA6MjgwYnI1MjAxOjcwMTU5MTE0MTUwOA==",
}


def main(date: str, time: str, court: int = 3, duration: int = 90) -> None:
    with open("auth_headers.json", "r") as f:
        headers = json.load(f)
    headers["Content-Type"] = "application/json"

    reserve_url = "https://api.lifetimefitness.com/sys/registrations/V3/ux/resource"

    def to_central_time_iso(date: str, time: str) -> str:
        naive_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")

        tz = pytz.timezone("America/Chicago")  # well, St. Louis, but close enough
        local_dt = tz.localize(naive_datetime)

        return local_dt.isoformat()

    body = {
        "resourceId": COURT_IDS[court],
        "start": to_central_time_iso(date, time),
        "service": None,
        "duration": str(duration),
    }

    # Send the initial booking request
    response = requests.post(reserve_url, headers=headers, json=body)

    if response.ok:
        registration_id = response.json().get("regId")
        if not registration_id:
            print(
                "❌ No registration ID returned. The response shape may have changed."
            )
            return
        print("✅ Reservation pending! Now we just need to accept the waiver...")
    else:
        if response.status_code == 403 or response.status_code == 401:
            print(
                """❌ Authentication failed. Remember to run extract_authentication_headers.py first and confirm that it has all 4 keys:
                ocp-apim-subscription-key
                x-ltf-ssoid
                x-ltf-jwe
                x-ltf-profile
                """
            )
        elif response.status_code == 500:
            print("❌ Server error. Try again just in case.")
            print(response.content)
        else:
            print(
                f"❌ Initial reservation request failed with status {response.status_code}"
            )
            print(response.content)
        return

    # Accept waiver / complete booking
    complete_url = f"https://api.lifetimefitness.com/sys/registrations/V3/ux/resource/{registration_id}/complete"
    complete_payload = {
        "acceptedDocuments": [73]
    }  # this is the waiver ID, but who knows what it is or whether it will change

    print(
        f"📝 Completing reservation for {date} at {time} for {duration} minutes on court {court}."
    )

    response = requests.put(complete_url, headers=headers, json=complete_payload)
    if response.ok:
        print("✅ Reservation complete!")
    else:
        print(
            f"❌ Reservation completion request failed with status {response.status_code}"
        )
        return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--date",
        type=str,
        required=True,
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
    main(date=args.date, time=args.time, court=args.court, duration=args.duration)
