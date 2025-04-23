import os
from pathlib import Path

from dotenv import load_dotenv
from playwright.sync_api import BrowserContext, sync_playwright

AUTH_FILE = "auth.json"


def get_authenticated_context(playwright, headless=True) -> BrowserContext:
    load_dotenv()

    username = os.getenv("ACCOUNT_USERNAME")
    password = os.getenv("ACCOUNT_PASSWORD")

    if Path(AUTH_FILE).exists():
        try:
            context = playwright.chromium.launch_persistent_context(
                user_data_dir="/tmp/playwright",
                headless=headless,
                storage_state=AUTH_FILE,
            )
            page = context.new_page()
            page.goto(
                "https://my.lifetime.life/account/reservations.html", timeout=5000
            )
            if page.url.startswith("https://my.lifetime.life/account"):
                return context
        except Exception as e:
            print(f"⚠️ Failed to reuse session: {e}")

    # Login fresh and save state
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://my.lifetime.life/login.html")

    page.fill("input#account-username", username)
    page.fill("input#account-password", password)
    page.click("button#login-btn")

    # Wait for successful login
    page.wait_for_url("**/home.html", timeout=10000)

    context.storage_state(path=AUTH_FILE)
    browser.close()

    # Re-open context in headless mode for actual work
    return playwright.chromium.launch_persistent_context(
        user_data_dir="/tmp/playwright",
        headless=headless,
        storage_state=AUTH_FILE,
    )
