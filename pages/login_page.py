import re
import time
from urllib.parse import urlsplit

from pages.base_page import BasePage
from playwright.sync_api import expect
from playwright.sync_api import (
    TimeoutError as PlaywrightTimeoutError,
    expect
)


class LoginPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

        # Login input fields.
        self.username_field = self.page.locator(
            "input[name='signin-username']"
        )
        self.password_field = self.page.locator(
            "input[name='signin-password']"
        )

        # Login Submit button.
        self.submit_button = self.page.get_by_role(
            "button", name="Submit"
        )

        # Login network diagnostics.
        self.login_response_statuses = []
        self.login_request_failures = 0
        self._login_response_handler = None
        self._login_failure_handler = None

    # ==========================================
    # OPEN LOGIN PAGE
    # ==========================================

    def open_login_page(self):

        self.navigate("https://qa.gct.com/account/signin")

        # Ensure credentials are entered only on the QA domain.
        actual_host = urlsplit(self.page.url).hostname

        if actual_host != "qa.gct.com":
            raise AssertionError(
                "Browser redirected away from the GCT QA website."
            )

        self.page.wait_for_load_state("domcontentloaded")

        # Handle cookie consent and promotional popups.
        self.accept_cookies()
        print("Cookie consent handling completed.")

        self.close_promo_popup()

        # Wait for the username field.
        expect(self.username_field).to_be_visible(
            timeout=15000
        )

        # Do not apply CSS that hides the entered values.
        print("GCT login page is ready!")

    # ==========================================
    # ENTER USERNAME
    # ==========================================

    def enter_username(self, username):

        self.username_field.scroll_into_view_if_needed()

        if not self.username_field.is_editable():
            self.username_field.click()

            expect(self.username_field).to_be_editable(
                timeout=10000
            )

        self.username_field.fill(username)

        # Verify the actual value in the browser field.
        username_matches = self.username_field.evaluate(
            "(element, expected) => element.value === expected",
            username
        )

        if not username_matches:
            raise AssertionError(
                "Username field did not retain the supplied value."
            )

        print("Username field verified; value hidden in logs.")

    # ==========================================
    # ENTER PASSWORD
    # ==========================================

    def enter_password(self, password):

        self.password_field.scroll_into_view_if_needed()

        if not self.password_field.is_editable():
            self.password_field.click()

            expect(self.password_field).to_be_editable(
                timeout=10000
            )

        # Type character by character to trigger manual keyboard events.
        self.password_field.fill("")
        self.password_field.press_sequentially(
            password,
            delay=20
        )

        # Verify the actual value without displaying it.
        password_matches = self.password_field.evaluate(
            "(element, expected) => element.value === expected",
            password
        )

        if not password_matches:
            raise AssertionError(
                "Password field did not retain the supplied value."
            )

        print("Password field verified; value hidden in logs.")

    # ==========================================
    # CLICK SUBMIT
    # ==========================================

    def click_submit(self):

        expect(self.submit_button).to_be_enabled(
            timeout=10000
        )

        self.submit_button.click()

        print("Login Submit button clicked!")

    # ==========================================
    # LOGIN WITH CREDENTIALS
    # ==========================================

    def login_with_valid_credentials(self, username, password):

        # Safe diagnostics: never print actual credentials.
        print("Username received:", bool(username))
        print("Password received:", bool(password))
        print("Username length:", len(username))
        print("Password length:", len(password))
        print(
            "Username has surrounding spaces:",
            username != username.strip()
        )
        print(
            "Password has surrounding spaces:",
            password != password.strip()
        )

        # Stop before submission if accidental surrounding spaces exist.
        if username != username.strip():
            raise AssertionError(
                "Username contains leading or trailing spaces."
            )

        if password != password.strip():
            raise AssertionError(
                "Password contains leading or trailing spaces."
            )

        # Enter and verify both credentials.
        self.enter_username(username)
        self.enter_password(password)

        # Start collecting network information before submission.
        self._start_login_diagnostics()

        self.click_submit()

        print("Login credentials submitted!")

    # ==========================================
    # START NETWORK DIAGNOSTICS
    # ==========================================

    def _start_login_diagnostics(self):

        self.login_response_statuses = []
        self.login_request_failures = 0

        def is_gct_request(request):

            host = urlsplit(request.url).hostname or ""

            return (
                host == "gct.com"
                or host.endswith(".gct.com")
            )

        def record_response(response):

            if (
                response.request.method.upper() == "POST"
                and is_gct_request(response.request)
            ):
                self.login_response_statuses.append(
                    response.status
                )

        def record_failure(request):

            if (
                request.method.upper() == "POST"
                and is_gct_request(request)
            ):
                self.login_request_failures += 1

        self._login_response_handler = record_response
        self._login_failure_handler = record_failure

        self.page.on("response", record_response)
        self.page.on("requestfailed", record_failure)

    # ==========================================
    # STOP NETWORK DIAGNOSTICS
    # ==========================================

    def _stop_login_diagnostics(self):

        if self._login_response_handler is not None:

            self.page.remove_listener(
                "response",
                self._login_response_handler
            )

            self._login_response_handler = None

        if self._login_failure_handler is not None:

            self.page.remove_listener(
                "requestfailed",
                self._login_failure_handler
            )

            self._login_failure_handler = None

    # ==========================================
    # NETWORK DIAGNOSTIC SUMMARY
    # ==========================================

    def _login_diagnostic_summary(self):

        if self.login_request_failures:

            network_status = (
                f"{self.login_request_failures} "
                "GCT POST request(s) failed."
            )

        elif self.login_response_statuses:

            statuses = ", ".join(
                str(status)
                for status in self.login_response_statuses
            )

            network_status = (
                f"GCT POST response status(es): {statuses}."
            )

        else:

            network_status = (
                "No completed GCT POST response was observed."
            )

        if self.page.is_closed():
            submit_status = "Submit state unavailable; login page is closed."
        elif self.submit_button.count() == 0:
            submit_status = "Submit button is not present."
        else:
            try:
                submit_enabled = self.submit_button.is_enabled(
                    timeout=1000
                )
            except PlaywrightTimeoutError:
                submit_status = "Submit state could not be determined."
            else:
                if submit_enabled:
                    submit_status = "Submit is enabled."
                else:
                    submit_status = "Submit is disabled or loading."

        return f"{network_status} {submit_status}"

    # ==========================================
    # VERIFY SUCCESSFUL LOGIN
    # ==========================================

    
    def verify_successful_login(self):
        """
        Verify successful login using the visible My Account heading.
        Use the heading role to avoid matching hidden duplicate text.
        """
        try:
            # Wait until the account overview page is loaded.
            expect(self.page).to_have_url(
                re.compile(r".*/my-account/overview/?$"),
                timeout=20000
            )

            # Locate only the actual visible Welcome heading.
            welcome_heading = self.page.get_by_role(
                "heading",
                name=re.compile(r"^Welcome,\s+\S+$")
            )

            # Verify that the heading is visible.
            expect(welcome_heading).to_be_visible(timeout=20000)

            print("Login successful!")
            print("My Account dashboard verified!")

        except Exception as error:
            print("Login verification failed.")
            print("Current URL:", self.page.url)
            print("Actual error:", repr(error))

            raise AssertionError(
                f"Login verification failed: {error}"
            ) from error

        finally:
            self._stop_login_diagnostics()
