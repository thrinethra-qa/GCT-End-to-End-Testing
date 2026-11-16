
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from pages.base_page import BasePage


class HomePage(BasePage):

    def __init__(self, page):
        # Initialize common browser methods from BasePage.
        super().__init__(page)

    def open_homepage(self):
        # Navigate to the GCT homepage.
        self.navigate("https://www.gct.com/")

    def click_logo(self):
        # Locate the visible GCT logo and click it.
        self.page.locator(
            ".global-header-logo a:visible"
        ).click()

        # Verify that the browser returns to the homepage.
        self.page.wait_for_url(
            "https://www.gct.com/",
            timeout=15000
        )

    def open_special_offers(self):

        # Close the promotional popup if it is already visible.
        self.close_promo_popup()

        # Locate the visible Special Offers navigation link.
        # Using the href helps avoid selecting an unrelated duplicate link.
        special_offer = self.page.locator(
            "a[href*='/special-offers']:visible"
        ).first

        # Wait until the navigation link is visible.
        special_offer.wait_for(
            state="visible",
            timeout=15000
        )

        # Check whether we are already on the Special Offers page.
        if "/special-offers" in self.page.url:
            print("Already on the Special Offers page.")
            return

        # Try clicking the navigation link.
        try:
            special_offer.click(timeout=10000)

        except PlaywrightTimeoutError:

            # The click may be blocked by a promotional popup.
            print(
                "Special Offers click timed out. "
                "Checking for a promotional popup..."
            )

            # Close the popup if it appears after the first attempt.
            self.close_promo_popup(
                wait_timeout=3000
            )

            # Do not click again if the first click already navigated.
            if "/special-offers" not in self.page.url:

                print("Retrying the Special Offers navigation.")

                special_offer.click(
                    timeout=15000
                )

        # Wait for the Special Offers URL.
        try:
            self.page.wait_for_url(
                "**/special-offers**",
                timeout=30000
            )

        except PlaywrightTimeoutError:

            # Print the current URL to help identify navigation problems.
            print(
                "Special Offers navigation failed. "
                f"Current URL: {self.page.url}"
            )

            raise

        print(
            "Special Offers navigation completed successfully!"
        )
