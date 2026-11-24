
from pathlib import Path
import os
from playwright.sync_api import sync_playwright


def before_all(context):

    # Start Playwright.
    context.playwright = sync_playwright().start()

    # Detect whether tests are running in GitHub Actions.
    context.is_ci = os.getenv("CI", "false").lower() == "true"

    # Launch Chromium.
    # Locally: visible browser.
    # CI: headless browser.
    context.browser = context.playwright.chromium.launch(
        headless=context.is_ci,
        args=["--start-maximized"] if not context.is_ci else []
    )

    print(f"Playwright browser launched successfully! CI mode: {context.is_ci}")


def before_scenario(context, scenario):

    # Create a separate browser context for each scenario.
    if context.is_ci:

        # CI: use a fixed desktop viewport.
        context.browser_context = context.browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir="videos/"
        )

    else:

        # Local: preserve the existing browser window behavior.
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

        # Create screenshots folder if it does not exist.
        Path("screenshots").mkdir(
            parents=True,
            exist_ok=True
        )

        # Create a safe screenshot filename.
        safe_name = "".join(
            c if c.isalnum() or c in ("-", "_") else "_"
            for c in scenario.name
        )

        # Capture the failed page.
        context.page.screenshot(
            path=f"screenshots/{safe_name}.png",
            full_page=True
        )

        print(f"Failure screenshot saved: {safe_name}.png")

    # Close browser context and finalize video.
    if hasattr(context, "browser_context"):
        context.browser_context.close()


def after_all(context):

    # Close browser.
    if hasattr(context, "browser"):
        context.browser.close()

    # Stop Playwright.
    if hasattr(context, "playwright"):
        context.playwright.stop()

    print("Playwright browser closed successfully!")
