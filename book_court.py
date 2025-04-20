import argparse
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright


class PickleBooker:

    def __init__(self, date: str, start_hour: int, end_hour: int):
        self.date = date
        self.start_hour = start_hour
        self.end_hour = end_hour

    def book_slot(self):
        load_dotenv()

        username = os.getenv("ACCOUNT_USERNAME")
        password = os.getenv("ACCOUNT_PASSWORD")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto("https://my.lifetime.life/login.html")
            page.locator("input[id='account-username']").fill(username)
            page.locator("input[id='account-password']").fill(password)
            with page.expect_navigation():
                page.locator("button[id='login-btn']").click()
            page.goto(
                self._format_booking_url(
                    date=self.date,
                )
            )

            slot = self._find_available_timeslot(page, self.start_hour, self.end_hour)

            if not slot:
                return
    
            slot.evaluate("el => el.style.outline = '3px solid hotpink'")
            page.wait_for_timeout(4000)
            with page.expect_navigation():
                slot.click()
            page.wait_for_timeout(4000)
            page.click("label[for='acceptwaiver']")
            page.wait_for_timeout(2000)
            with page.expect_navigation():
                page.locator("button:has-text('Finish')").click()
            page.wait_for_timeout(4000)
            page.pause()

    def _format_booking_url(self, date: str):
        base_url = "https://my.lifetime.life/clubs/mo/frontenac/resource-booking.html"
        params = {
            "sport": "Pickleball: Indoor",
            "clubId": 280,
            "date": date,
            "startTime": -1,
            "duration": 90,
            "hideModal": "true",
        }
        url = f"{base_url}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"
        return url
    
    def _find_available_timeslot(self, page, start_hour: int, end_hour: int):
        current = datetime.today().replace(hour=start_hour, minute=0)
        end = current.replace(hour=end_hour, minute=0)   
        while current <= end:
            label = current.strftime("%I:%M %p").lstrip("0")  # e.g. "9:00 AM", "3:30 PM"

            selector = f"a.timeslot:has-text('{label}')"

            try:
                slot = page.wait_for_selector(selector, timeout=5000)
                return slot
            except Exception:
                current += timedelta(minutes=30)

        return None 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--date",
        type=str,
        help="Date to book the court (YYYY-MM-DD)",
        required=True,

    )
    parser.add_argument(
        "--start-gte",
        type=int,
        help="Start hour for booking range (0-23)",
        required=True,
    )
    parser.add_argument(
        "--start-lte",
        type=int,
        help="End hour for booking range (0-23)",
        required=True,
    )
    PickleBooker(
        date=parser.parse_args().date,
        start_hour=parser.parse_args().start_gte,
        end_hour=parser.parse_args().start_lte,
    ).book_slot()
