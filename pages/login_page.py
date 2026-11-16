import re

from pages.base_page import BasePage
from playwright.sync_api import expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


class LoginPage(BasePage):

    def __init__(self, page):

        # Initialize the common methods from BasePage.
        super().__init__(page)

        # Locator for the username/email input field.
        self.username_field = self.page.locator(
            "input[name='signin-username']"
        )

        # Locator for the password input field.
        self.password_field = self.page.locator(
            "input[name='signin-password']"
        )

        # Locator for the Submit button.
        self.submit_button = self.page.get_by_role(
            "button",
            name="Submit"
        )

        # Locator for the Black Friday promotional popup close button.
        self.promo_close_button = self.page.locator(
            "form#WebPop button:has(span.icon-close-rounded)"
        )

        # Locator for the invalid login error message.
        self.login_error_message = self.page.get_by_text(
            re.compile(
                r"Your username or password is incorrect. Please try resetting your username and then password if this persists.",
                re.IGNORECASE
            )
        )

    def open_login_page(self):

        # Navigate to the GCT login page.
        self.navigate(
            "https://www.gct.com/account/signin"
        )

        # Wait until the initial page content is loaded.
        self.page.wait_for_load_state(
            "domcontentloaded"
        )

        # Accept cookies if the consent dialog appears.
        self.accept_cookies()

        # The promotional popup must appear within 30 seconds,
        # otherwise the test fails.
        self.wait_and_close_promo_popup()

        # Wait until the username field is visible.
        expect(
            self.username_field
        ).to_be_visible(timeout=15000)

        # Inspect the username field before entering credentials.
        self.inspect_username_field()

        print("GCT login page opened successfully!")

    def inspect_username_field(self):

        # Read the actual properties of the username field
        # directly from the browser DOM.
        field_details = self.username_field.evaluate(
            """element => ({
                type: element.type,
                readOnly: element.readOnly,
                disabled: element.disabled,
                value: element.value,
                outerHTML: element.outerHTML
            })"""
        )

        # Print the username field details in the terminal.
        print("\n========== USERNAME FIELD DETAILS ==========")

        for key, value in field_details.items():
            print(f"{key}: {value}")

        print("============================================\n")

        # Also check the field using Playwright methods.
        print(
            "Username field visible:",
            self.username_field.is_visible()
        )

        print(
            "Username field enabled:",
            self.username_field.is_enabled()
        )

        print(
            "Username field editable:",
            self.username_field.is_editable()
        )

    def inspect_field(self, field, label):

        # Print what Playwright finds, without hanging if nothing matches.
        count = field.count()
        print(f"\n===== {label}: {count} element(s) found =====")

        if count == 0:
            print("Locator matched nothing. The locator is probably wrong.")
            return

        details = field.first.evaluate(
            """element => ({
                type: element.type,
                readOnly: element.readOnly,
                disabled: element.disabled,
                outerHTML: element.outerHTML
            })"""
        )

        for key, value in details.items():
            print(f"{key}: {value}")

        print("=========================================\n")

    def wait_and_close_promo_popup(self):

        # Wait up to 30 seconds for the promotional popup to appear.
        try:
            self.promo_close_button.wait_for(
                state="visible",
                timeout=30000
            )
        except PlaywrightTimeoutError:
            # Fail the test if the popup never appears.
            raise AssertionError(
                "Promotional popup did not appear within 30 seconds."
            )

        # Close the promotional popup.
        self.promo_close_button.click(
            timeout=5000
        )

        # Wait until the popup close button disappears.
        self.promo_close_button.wait_for(
            state="hidden",
            timeout=5000
        )

        print("Promotional popup closed successfully!")

    def close_promo_popup(self):

        # Lenient check: close the popup only if it appears.
        try:

            self.promo_close_button.wait_for(
                state="visible",
                timeout=3000
            )

            # Close the promotional popup.
            self.promo_close_button.click(
                timeout=5000
            )

            # Wait until the popup close button disappears.
            self.promo_close_button.wait_for(
                state="hidden",
                timeout=5000
            )

            print("Promotional popup closed successfully!")

        except PlaywrightTimeoutError:

            # Continue if the promotional popup is not displayed
            # or its close button is unavailable.
            print(
                "Promotional popup is not displayed "
                "or could not be closed."
            )

    def enter_username(self, username_value):

        # Close the promotional popup if it appears.
        self.close_promo_popup()

        # Make sure the field is in view.
        self.username_field.scroll_into_view_if_needed()

        try:
            # Auto-retrying check, unlike is_editable().
            expect(self.username_field).to_be_editable(timeout=5000)

        except AssertionError:
            # Some sites keep the field readonly until it is focused.
            self.username_field.click()

            try:
                expect(self.username_field).to_be_editable(timeout=10000)
            except AssertionError:
                self.inspect_username_field()
                raise AssertionError(
                    "Username field is still not editable after click. "
                    "Check readOnly/disabled in the printed field details."
                )

        # Enter the username/email.
        self.username_field.fill(username_value)

        print("Username entered successfully!")

    def enter_password(self, password_value):

        # Make sure the field is in view.
        self.password_field.scroll_into_view_if_needed()

        try:
            # Auto-retrying check.
            expect(self.password_field).to_be_editable(timeout=5000)

        except AssertionError:
            # Some sites keep the field readonly until it is focused.
            self.password_field.click()

            try:
                expect(self.password_field).to_be_editable(timeout=10000)
            except AssertionError:
                self.inspect_field(self.password_field, "PASSWORD FIELD")
                raise AssertionError(
                    "Password field is not editable. "
                    "Check the printed PASSWORD FIELD details."
                )

        # Enter the password.
        self.password_field.fill(password_value)

        print("Password entered successfully!")

    def click_submit(self):

        # Show how many Submit buttons the locator matches.
        self.inspect_field(self.submit_button, "SUBMIT BUTTON")

        # Use the first match to avoid strict-mode errors
        # when more than one button is named "Submit".
        button = self.submit_button.first

        button.scroll_into_view_if_needed()

        # Wait until the button is enabled.
        expect(button).to_be_enabled(timeout=10000)

        # Click the Submit button.
        button.click()

        print("Login Submit button clicked!")

    def is_login_error_displayed(self):


        # Verify that the invalid login error message is displayed.
        expect(
            self.login_error_message
        ).to_be_visible(timeout=15000)

        print(
            "Invalid login error message displayed successfully!"
        )

        return True