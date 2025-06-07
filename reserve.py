import argparse
import json
import os
import time
from datetime import datetime

import pytz
import requests

from extract_authentication_headers import AUTH_HEADERS_PATH

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

COURT_IDS = {
    1: "ZXhlcnA6MjgwYnI0ODAxOjcwMTU5MTE0MTUwOA==",
    2: "ZXhlcnA6MjgwYnI1MDAxOjcwMTU5MTE0MTUwOA==",
    3: "ZXhlcnA6MjgwYnI1MjAxOjcwMTU5MTE0MTUwOA==",
}

MAX_RETRIES = 20
RETRY_DELAY = 0.2  # seconds


def make_request_with_retries(
    method: str,
    url: str,
    headers: dict,
    payload: dict | None = None,
    retries: int = MAX_RETRIES,
) -> requests.Response:
    for attempt in range(retries):
        if method.upper() == "POST":
            response = requests.post(url, headers=headers, json=payload)
        elif method.upper() == "PUT":
            response = requests.put(url, headers=headers, json=payload)
        else:
            raise ValueError(f"Unsupported method: {method}")

        if response.ok:
            return response
        elif response.status_code in {401, 403}:
            print(
                """
                ❌ Authentication failed. Remember to run extract_authentication_headers.py first and confirm that it has all 4 keys:
                    - ocp-apim-subscription-key
                    - x-ltf-ssoid
                    - x-ltf-jwe
                    - x-ltf-profile
                """
            )
            raise SystemExit(1)
        elif response.status_code == 500:
            print(f"❌ Server error on attempt {attempt+1}. Retrying...")
            time.sleep(RETRY_DELAY)
        else:
            print(f"❌ Request failed with status {response.status_code}")
            print(f"Response: {response.text}")
            raise SystemExit(1)

    print("❌ Max retries exceeded.")
    raise SystemExit(1)


def post_reservation(payload: dict, headers: dict) -> requests.Response:
    reserve_url = "https://api.lifetimefitness.com/sys/registrations/V3/ux/resource"
    print(
        f"Making reservation request for {payload['start']} for {payload['duration']} minutes on court {payload['resourceId']}"
    )
    response = make_request_with_retries(
        method="POST",
        url=reserve_url,
        headers=headers,
        payload=payload,
    )
    return response


def complete_reservation(registration_id: str, headers: dict) -> requests.Response:
    complete_url = f"https://api.lifetimefitness.com/sys/registrations/V3/ux/resource/{registration_id}/complete"
    print(f"Completing reservation for {registration_id}")
    complete_payload = {
        "acceptedDocuments": [73]
    }  # this is the waiver ID, but who knows what it is or whether it will change
    response = make_request_with_retries(
        method="PUT",
        url=complete_url,
        headers=headers,
        payload=complete_payload,
    )
    return response


def to_central_time_iso(date: str, time: str) -> str:
    naive_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")

    tz = pytz.timezone("America/Chicago")  # well, St. Louis, but close enough
    local_dt = tz.localize(naive_datetime)

    return local_dt.isoformat()


def reserve(date: str, time: str, court: int = 3, duration: int = 90) -> None:
    with open(os.path.join(BASE_DIR, AUTH_HEADERS_PATH), "r") as f:
        headers = json.load(f)
    headers["Content-Type"] = "application/json"

    body = {
        "resourceId": COURT_IDS[court],
        "start": to_central_time_iso(date, time),
        "service": None,
        "duration": str(duration),
    }

    # Make initial reservation request
    response = post_reservation(body, headers)

    registration_id = response.json().get("regId")
    if not registration_id:
        print(
            "❌ Failed to get registration ID from response. Response shape may have changed."
        )
        print("Response:", response.json())
        return

    print(f"✅ Reservation ID: {registration_id}")

    # Accept waiver / complete booking
    complete_reservation(registration_id, headers)
    print("✅ Reservation complete!")

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
    reserve(date=args.date, time=args.time, court=args.court, duration=args.duration)
