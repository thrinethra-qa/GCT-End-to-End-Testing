
import re

from playwright.sync_api import expect

from pages.base_page import BasePage


class HomePage(BasePage):
    def open_homepage(self):
        self.navigate("https://qa.gct.com/")

    def search_for_europe(self):
        self.accept_cookies()
        self.close_promo_popup()

        expect(
            self.page.get_by_role("heading", name="Find Your Trip")
        ).to_be_visible(timeout=15000)

        self.page.get_by_role(
            "button",
            name="Destination",
            exact=True
        ).click()

        destination_dialog = self.page.get_by_role(
            "dialog",
            name="Destination"
        )
        search_box = destination_dialog.get_by_role(
            "searchbox",
            name="Search destinations"
        )
        search_box.fill("Europe")

        europe_checkbox = destination_dialog.get_by_role(
            "checkbox",
            name=re.compile(r"^Europe(?:\s|$)")
        )
        if not europe_checkbox.is_checked():
            europe_checkbox.check()

        destination_dialog.get_by_role(
            "button",
            name="Apply",
            exact=True
        ).click()

        self.page.get_by_role(
            "button",
            name="Search for trips",
            exact=True
        ).click()

        expect(self.page).to_have_url(
            re.compile(r"/tripsavailable"),
            timeout=30000
        )
