
import os
import re
from pathlib import Path

from playwright.sync_api import sync_playwright


def _report_evidence_error(action, error):
    print(
        f"Could not {action}; original scenario result is preserved "
        f"({type(error).__name__})."
    )


def before_all(context):
    context.playwright = sync_playwright().start()
    context.is_ci = os.getenv("CI", "false").lower() == "true"
    context.screenshot_dir = Path("screenshots")
    context.video_dir = Path("videos")
    context.trace_dir = Path("traces")
    context.video_dir.mkdir(parents=True, exist_ok=True)
    context.trace_dir.mkdir(parents=True, exist_ok=True)

    context.browser = context.playwright.chromium.launch(
        headless=context.is_ci,
        args=["--start-maximized"] if not context.is_ci else []
    )

    print(f"Chromium launched. Headless mode: {context.is_ci}")


def before_scenario(context, scenario):
    context.safe_scenario_name = re.sub(
        r"[^A-Za-z0-9_-]+",
        "_",
        scenario.name
    ).strip("_")

    if context.is_ci:
        context.browser_context = context.browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=str(context.video_dir)
        )
    else:
        context.browser_context = context.browser.new_context(
            no_viewport=True,
            record_video_dir=str(context.video_dir)
        )

    # Keep tracing free of screenshots and DOM values that could expose login data.
    context.browser_context.tracing.start(
        screenshots=False,
        snapshots=False,
        sources=False
    )
    context.tracing_started = True
    context.page = context.browser_context.new_page()
    print(f"Starting scenario: {scenario.name}")


def after_scenario(context, scenario):
    safe_name = getattr(
        context,
        "safe_scenario_name",
        "gct-demo"
    )

    if scenario.status in ("failed", "error"):
        page = getattr(context, "page", None)
        if page is not None and not page.is_closed():
            try:
                context.screenshot_dir.mkdir(parents=True, exist_ok=True)
                screenshot_path = context.screenshot_dir / f"{safe_name}.png"
                page.screenshot(
                    path=str(screenshot_path),
                    full_page=True,
                    mask=[
                        page.locator("input[name='signin-username']"),
                        page.locator("input[name='signin-password']")
                    ],
                    mask_color="#000000"
                )
                print(f"Failure screenshot saved: {screenshot_path}")
            except Exception as error:
                _report_evidence_error("save the failure screenshot", error)
        else:
            print(
                "Failure screenshot unavailable because the browser "
                "page is closed."
            )

    if getattr(context, "tracing_started", False):
        try:
            trace_path = context.trace_dir / f"{safe_name}.zip"
            context.browser_context.tracing.stop(path=str(trace_path))
            print(f"Playwright trace saved: {trace_path}")
        except Exception as error:
            _report_evidence_error("save the Playwright trace", error)
        finally:
            context.tracing_started = False

    browser_context = getattr(context, "browser_context", None)
    if browser_context is not None:
        try:
            # Closing the context also finalizes its recorded browser video.
            browser_context.close()
        except Exception as error:
            _report_evidence_error("close the browser context", error)


def after_all(context):
    browser = getattr(context, "browser", None)
    if browser is not None and browser.is_connected():
        try:
            browser.close()
        except Exception as error:
            _report_evidence_error("close the browser", error)

    playwright = getattr(context, "playwright", None)
    if playwright is not None:
        try:
            playwright.stop()
        except Exception as error:
            _report_evidence_error("stop Playwright", error)

    print("Playwright browser closed.")
