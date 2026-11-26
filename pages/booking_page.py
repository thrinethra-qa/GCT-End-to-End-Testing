import re

from playwright.sync_api import expect

from pages.base_page import BasePage


class BookingPage(BasePage):
    def open_dates_and_prices(self):
        self.close_promo_popup()
        self.page.get_by_role(
            "link",
            name="View Dates & Prices",
            exact=True
        ).click()
        expect(self.page).to_have_url(
            re.compile(r"/availabledatesandprices"),
            timeout=30000
        )
        self.close_promo_popup()

    def select_departure_year(self, year):
        self.close_promo_popup()
        year_filter = self.page.get_by_role(
            "button",
            name=re.compile(r"^Year filter:")
        )
        expect(year_filter).to_be_visible(timeout=15000)
        year_filter.click()

        year_option = self.page.get_by_role(
            "menuitemcheckbox",
            name=str(year),
            exact=True
        )
        expect(year_option).to_be_visible(timeout=10000)
        year_option.click()

    def select_departure_date(self):
        self.close_promo_popup()
        departure_month = self.page.get_by_role(
            "button",
            name=re.compile(r"^.+From.+View Dates", re.DOTALL)
        ).first
        expect(departure_month).to_be_visible(timeout=15000)
        departure_month.click()

        date_button = self.page.get_by_role(
            "button",
            name="Select Date",
            exact=True
        )
        expect(date_button).to_be_visible(timeout=15000)
        date_button.click()

    def select_cabin(self):
        self.close_promo_popup()
        select_cabins_button = self.page.get_by_role(
            "button",
            name="Select Cabins",
            exact=True
        ).first
        expect(select_cabins_button).to_be_visible(timeout=15000)
        select_cabins_button.click()
        self.close_promo_popup()

        selected_cabin = self.page.get_by_role(
            "button",
            name="Selected",
            exact=True
        )
        expect(selected_cabin).to_be_visible(timeout=10000)

        next_button = self.page.get_by_role(
            "button",
            name=re.compile(r"^Next: Pricing Summary")
        )
        expect(next_button).to_be_enabled(timeout=15000)

    def continue_to_pricing_summary(self):
        self.close_promo_popup()
        next_button = self.page.get_by_role(
            "button",
            name=re.compile(r"^Next: Pricing Summary")
        )
        expect(next_button).to_be_enabled(timeout=15000)
        next_button.click()
        pricing_summary_tab = self.page.get_by_role(
            "tab",
            name=re.compile(r"Pricing Summary")
        )
        expect(pricing_summary_tab).to_have_attribute(
            "aria-selected",
            "true",
            timeout=20000
        )
        save_button = self.page.get_by_role(
            "button",
            name=re.compile(r"Save Pricing Summary$")
        )
        expect(save_button).to_be_visible(timeout=20000)

    def _no_travel_protection_choice(self):
        return self.page.get_by_role(
            "radio",
            name="No, I do not want travel protection",
            exact=True
        )

    def select_no_travel_protection(self):
        self.close_promo_popup()
        protection_choice = self._no_travel_protection_choice()
        expect(protection_choice).to_be_visible(timeout=15000)
        protection_choice.check()
        expect(protection_choice).to_be_checked()

    def save_pricing_summary(self):
        self.close_promo_popup()
        expect(
            self._no_travel_protection_choice()
        ).to_be_checked(timeout=10000)
        save_button = self.page.get_by_role(
            "button",
            name=re.compile(r"Save Pricing Summary$")
        )
        expect(save_button).to_be_enabled(timeout=15000)
        save_button.click()
