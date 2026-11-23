
from pathlib import Path
import os
from playwright.sync_api import sync_playwright


def before_all(context):

    # Start Playwright.
    context.playwright = sync_playwright().start()

    # Detect whether the tests are running in GitHub Actions or another CI environment.
    # GitHub Actions automatically sets the CI environment variable to "true".
    is_ci = os.getenv("CI", "false").lower() == "true"

    # Launch Chromium.
    # Locally: headless=False (browser is visible).
    # In CI: headless=True (browser runs without a graphical window).
    context.browser = context.playwright.chromium.launch(
        headless=is_ci,
        args=["--start-maximized"] if not is_ci else []
    )

    print(f"Playwright browser launched successfully! CI mode: {is_ci}")


def before_scenario(context, scenario):

    # Create a new browser context for each scenario.
    # Locally, no_viewport=True allows the browser to use the actual window size.
    # Videos are recorded for each scenario.
    context.browser_context = context.browser.new_context(
        no_viewport=True,
        record_video_dir="videos/"
    )

    # Create a new page for the current scenario.
    context.page = context.browser_context.new_page()

    print(f"Starting scenario: {scenario.name}")


def after_scenario(context, scenario):

    # Save a screenshot when a scenario fails.
    if scenario.status == "failed" and hasattr(context, "page"):

        # Create the screenshots folder if it does not exist.
        Path("screenshots").mkdir(
            parents=True,
            exist_ok=True
        )

        # Replace special characters in the scenario name with underscores.
        safe_name = "".join(
            c if c.isalnum() or c in ("-", "_") else "_"
            for c in scenario.name
        )

        # Save the failure screenshot.
        context.page.screenshot(
            path=f"screenshots/{safe_name}.png",
            full_page=True
        )

        print(f"Failure screenshot saved: {safe_name}.png")

    # Close the browser context.
    # This also finalizes the recorded video for the scenario.
    if hasattr(context, "browser_context"):
        context.browser_context.close()


def after_all(context):

    # Close the browser only if it was successfully launched.
    if hasattr(context, "browser"):
        context.browser.close()

    # Stop Playwright only if it was successfully started.
    if hasattr(context, "playwright"):
        context.playwright.stop()

    print("Playwright browser closed successfully!")
