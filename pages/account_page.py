
import re

from playwright.sync_api import expect
from pages.base_page import BasePage


class AccountPage(BasePage):

    def open_my_account(self):
        # The saved pricing summary may display a "View in My Account" button.
        view_account_button = self.page.get_by_role(
            "button",
            name="View in My Account",
            exact=True
        )

        # Click it only when the button is displayed.
        if view_account_button.is_visible():
            view_account_button.click()
            print("Clicked View in My Account from the saved summary popup.")

        # Confirm that the My Account page has loaded.
        expect(self.page).to_have_url(
            re.compile(r".*/my-account.*"),
            timeout=20000
        )

        print("My Account page opened successfully.")

    def verify_trip_is_added(self, trip_name):
        # Confirm that the Saved Trip Summaries section is displayed.
        expect(
            self.page.get_by_role(
                "heading",
                name="Saved Trip Summaries",
                exact=True
            )
        ).to_be_visible(timeout=15000)

        # Confirm that the expected trip title is displayed.
        expect(
            self.page.get_by_role(
                "heading",
                name=trip_name,
                exact=True
            ).first
        ).to_be_visible(timeout=15000)

        print(f"Saved trip summary verified: {trip_name}")

    def log_out(self):
        # Find the visible Sign Out button.
        # This avoids selecting a hidden duplicate button.
        sign_out_button = self.page.locator(
            "button:visible"
        ).filter(
            has_text=re.compile(r"^\s*Sign Out\s*$", re.IGNORECASE)
        )

        # If Sign Out is not visible, open the My Account dropdown.
        if sign_out_button.count() == 0:
            account_menu_button = self.page.get_by_role(
                "button",
                name=re.compile(r"My Account", re.IGNORECASE)
            ).first

            expect(account_menu_button).to_be_visible(timeout=10000)
            account_menu_button.click()

        # Wait for the visible Sign Out button and click it.
        expect(sign_out_button).to_be_visible(timeout=10000)
        sign_out_button.click()

        print("Clicked Sign Out successfully.")

    def verify_logged_out(self):
        # Verify that the user is redirected to the GCT login page.
        expect(self.page).to_have_url(
            re.compile(r".*/account/signin.*"),
            timeout=20000
        )

        print("Logout successful. GCT login page displayed.")
