import os
from pathlib import Path

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

AUTH_FILE = "auth.json"


def get_authenticated_context(playwright, headless=True) -> None:
    load_dotenv()

    username = os.getenv("ACCOUNT_USERNAME")
    password = os.getenv("ACCOUNT_PASSWORD")

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://my.lifetime.life/login.html")

    page.fill("input#account-username", username)
    page.fill("input#account-password", password)
    page.click("button#login-btn")

    page.wait_for_url("**/home.html", timeout=10000)

    context.storage_state(path=AUTH_FILE)
    browser.close()

    print("✅ Authenticated and saved session state.")


if __name__ == "__main__":

    with sync_playwright() as playwright:
        get_authenticated_context(playwright)
