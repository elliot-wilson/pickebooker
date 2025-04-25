import json
import os

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

OUTPUT_PATH = "auth_headers.json"
# this URL fetches active reservations, so we can be sure it has an API call
TARGET_URL = "https://my.lifetime.life/account/my-reservations.html"


def main():
    load_dotenv()
    username = os.getenv("ACCOUNT_USERNAME")
    password = os.getenv("ACCOUNT_PASSWORD")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        found_headers = {}

        def handle_route(route, request):
            nonlocal found_headers
            headers = request.headers
            # Grab only relevant headers
            for key in headers:
                if (
                    key.lower().startswith("x-ltf")
                    or key.lower() == "ocp-apim-subscription-key"
                ):
                    found_headers[key] = headers[key]
            route.continue_()

        context.route("**/*", handle_route)

        page.goto("https://my.lifetime.life/login.html")
        page.fill("input#account-username", username)
        page.fill("input#account-password", password)
        page.click("button#login-btn")
        page.wait_for_url("**/home.html", timeout=10000)

        page.goto(TARGET_URL)
        page.wait_for_timeout(3000)

        browser.close()

        if found_headers:
            with open(OUTPUT_PATH, "w") as f:
                json.dump(found_headers, f, indent=2)
            print(f"✅ Saved auth headers to {OUTPUT_PATH}")
        else:
            print("⚠️ Did not find any matching headers.")


if __name__ == "__main__":
    main()
