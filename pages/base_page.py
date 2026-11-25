
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


class BasePage:

    def __init__(self, page):
        # Store the Playwright page for all child page classes.
        self.page = page

    # ---------------------------------------------------------
    # Common browser navigation methods
    # ---------------------------------------------------------

    def navigate(self, url):
        # Wait for the initial HTML instead of all images,
        # advertisements, and third-party resources.
        self.page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000
        )

    def click(self, locator):
        # Click an element using its locator.
        self.page.locator(locator).click()

    def fill(self, locator, value):
        # Enter text into an input field.
        self.page.locator(locator).fill(value)

    def get_text(self, locator):
        # Return the visible text of an element.
        return self.page.locator(locator).inner_text()

    def is_visible(self, locator):
        # Check whether an element is visible.
        return self.page.locator(locator).is_visible()

    def go_back(self):
        # Navigate to the previous browser page.
        self.page.go_back(
            wait_until="domcontentloaded",
            timeout=60000
        )

    def go_forward(self):
        # Navigate to the next browser page.
        self.page.go_forward(
            wait_until="domcontentloaded",
            timeout=60000
        )

    # ---------------------------------------------------------
    # Cookie consent popup handling
    # ---------------------------------------------------------

    def accept_cookies(self):
        # Locate the cookie consent dialog.
        cookie_popup = self.page.get_by_role(
            "dialog",
            name="Cookie consent"
        )

        try:
            # Check whether the cookie popup appears.
            cookie_popup.wait_for(
                state="visible",
                timeout=5000
            )

            # Locate the Accept button inside the dialog.
            accept_button = cookie_popup.get_by_role(
                "button",
                name="Accept",
                exact=True
            )

            # Accept cookies.
            accept_button.click(timeout=5000)

            # Wait until the cookie dialog disappears.
            cookie_popup.wait_for(
                state="hidden",
                timeout=5000
            )

            print("Cookie consent accepted successfully!")
            return True

        except PlaywrightTimeoutError:
            # The cookie popup may not appear every time.
            print("Cookie consent popup was not displayed.")
            return False

    # ---------------------------------------------------------
    # Promotional popup handling
    # ---------------------------------------------------------

    
    def close_promo_popup(self, wait_timeout=3000):

        # Locate the promotional popup using its accessible dialog name.
        promo_dialog = self.page.get_by_role(
            "dialog",
            name="Save up to $3,000"
        )

        try:
            # Wait for the popup to appear.
            promo_dialog.wait_for(
                state="visible",
                timeout=wait_timeout
            )

            # Locate the close button using its unique CSS class.
            close_button = promo_dialog.locator(
                "button:has(span.icon-close-rounded)"
            )

            # Verify that the close button is visible.
            close_button.wait_for(
                state="visible",
                timeout=5000
            )

            # Close the promotional popup.
            close_button.click(timeout=5000)

            # Wait until the popup disappears.
            promo_dialog.wait_for(
                state="hidden",
                timeout=5000
            )

            print("Promotional popup closed successfully!")
            return True

        except PlaywrightTimeoutError:

            # The popup may not appear during every test.
            print("Promotional popup was not displayed.")
            return False
