from pathlib import Path
from playwright.sync_api import sync_playwright


def before_all(context):

    # Start Playwright.
    context.playwright = sync_playwright().start()

    # Launch Chromium in headed mode with a maximized window.
    context.browser = context.playwright.chromium.launch(
        headless=False,
        args=["--start-maximized"]
    )

    print("Playwright browser launched successfully!")


def before_scenario(context, scenario):

    # Create a new browser context without a fixed viewport.
    # This allows the browser to use the maximized window size.
    context.browser_context = context.browser.new_context(
        no_viewport=True,
        record_video_dir="videos/"
    )

    # Create a new page for the current scenario.
    context.page = context.browser_context.new_page()

    print(f"Starting scenario: {scenario.name}")


def after_scenario(context, scenario):

    # Save a screenshot when a scenario fails.
    if scenario.status == "failed":

        # Create the screenshots folder if it does not exist.
        Path("screenshots").mkdir(
            parents=True,
            exist_ok=True
        )

        # Replace special characters in the scenario name.
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
    # This also finalizes the recorded video.
    context.browser_context.close()


def after_all(context):

    # Close the browser.
    context.browser.close()

    # Stop Playwright.
    context.playwright.stop()

    print("Playwright browser closed successfully!")