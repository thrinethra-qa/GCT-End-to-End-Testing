
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


class BasePage:
    def __init__(self, page):
        self.page = page

    def navigate(self, url):
        self.page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000
        )

    def accept_cookies(self):
        cookie_popup = self.page.get_by_role(
            "dialog",
            name="Cookie consent"
        )
        try:
            cookie_popup.wait_for(
                state="visible",
                timeout=5000
            )
        except PlaywrightTimeoutError:
            print("Cookie consent popup was not displayed.")
            return False

        cookie_popup.get_by_role(
            "button",
            name="Accept",
            exact=True
        ).click(timeout=5000)
        cookie_popup.wait_for(state="hidden", timeout=5000)
        print("Cookie consent accepted successfully.")
        return True

    def close_promo_popup(self, wait_timeout=3000, report_absent=True):
        if self.page.is_closed():
            return False

        offer_text = self.page.get_by_text(
            "Save up to $3,000",
            exact=False
        )
        close_banner = self.page.get_by_role(
            "button",
            name="Close banner",
            exact=True
        )

        closed_popup = False
        if wait_timeout > 0:
            try:
                offer_text.wait_for(
                    state="visible",
                    timeout=wait_timeout
                )
            except PlaywrightTimeoutError:
                pass

        if offer_text.is_visible() and close_banner.is_visible():
            try:
                close_banner.click(timeout=5000)
                closed_popup = True
            except PlaywrightTimeoutError:
                # The site can remove the banner while its click is settling.
                if close_banner.is_visible():
                    raise
                closed_popup = True

        promo_dialog = self.page.get_by_role(
            "dialog",
            name="Save up to $3,000"
        )
        if promo_dialog.is_visible():
            dialog_close_button = promo_dialog.locator(
                "button:has(span.icon-close-rounded)"
            )
            if dialog_close_button.is_visible():
                dialog_close_button.click(timeout=5000)
                promo_dialog.wait_for(state="hidden", timeout=5000)
                print("Promotional signup dialog closed successfully!")
                closed_popup = True

        if closed_popup:
            print("Visible promotional content dismissed.")
            return True

        if report_absent:
            print("No promotional popup was displayed.")
        return False
