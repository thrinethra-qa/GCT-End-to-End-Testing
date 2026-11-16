
from behave import given, when, then

# Import the Page Object classes.
# These classes contain the actual browser actions and locators.
from pages.home_page import HomePage
from pages.search_page import SearchPage
from pages.login_page import LoginPage
from pages.signup_page import SignupPage
from pages.special_offers_page import SpecialOffersPage
from pages.river_europe_page import RiverEuropePage


# =====================================================
# COMMON HOMEPAGE STEP
# =====================================================

@given("the GCT homepage is opened")
def open_gct_homepage(context):

    # Create the HomePage object using the current browser page.
    context.home = HomePage(context.page)

    # Open the GCT website.
    context.home.open_homepage()


# =====================================================
# NAVIGATION TEST STEPS (TC01 - TC05)
# =====================================================

@when("I navigate to the Special Offers page")
def navigate_to_special_offers(context):

    # Navigate to the Special Offers page.
    context.home.open_special_offers()


@when("I click the GCT logo")
def click_gct_logo(context):

    # Click the GCT logo.
    context.home.click_logo()


@when("I click the browser back button")
def click_browser_back(context):

    # Navigate to the previous browser page.
    context.home.go_back()

    # Wait until the homepage URL is displayed.
    context.page.wait_for_url(
        "https://www.gct.com/",
        timeout=15000
    )


@when("I click the browser forward button")
def click_browser_forward(context):

    # Navigate forward in browser history.
    context.home.go_forward()

    # Wait until the Special Offers page opens.
    context.page.wait_for_url(
        "**/special-offers**",
        timeout=15000
    )


@then("the homepage should load successfully")
def verify_homepage(context):

    # Verify that the browser is on the GCT homepage.
    assert context.page.url.rstrip("/") == "https://www.gct.com", (
        "GCT homepage did not load successfully"
    )


@then("I should return to the homepage")
def verify_homepage_navigation(context):

    # Verify that clicking the logo returns to the homepage.
    assert context.page.url.rstrip("/") == "https://www.gct.com", (
        "Browser did not return to the homepage"
    )


@then("the Special Offers page should be displayed")
def verify_special_offers(context):

    # Verify that the Special Offers URL is displayed.
    assert "/special-offers" in context.page.url, (
        "Special Offers page was not displayed"
    )


# =====================================================
# DESTINATION SEARCH TEST STEPS (TC06 - TC09)
# =====================================================

# TC06 - Verify the destination search field is visible and enabled.
@then("the destination search field should be visible and enabled")
def verify_destination_search_visible_and_enabled(context):

    # Create the SearchPage object.
    search = SearchPage(context.page)

    # Verify that the destination search field is visible.
    assert search.is_search_visible(), (
        "Search field is not visible"
    )

    # Verify that the destination search field is enabled.
    assert search.is_search_enabled(), (
        "Search field is not enabled"
    )

    print("Destination search field is visible and enabled!")


# Separate visibility step, retained in case another scenario uses it.
@then("the destination search field should be visible")
def verify_search_visible(context):

    # Create the SearchPage object.
    search = SearchPage(context.page)

    # Verify search field visibility.
    assert search.is_search_visible(), (
        "Search field is not visible"
    )


# Separate enabled step, retained in case another scenario uses it.
@then("the destination search field should be enabled")
def verify_search_enabled(context):

    # Create the SearchPage object.
    search = SearchPage(context.page)

    # Verify search field enabled state.
    assert search.is_search_enabled(), (
        "Search field is not enabled"
    )


@when('I search for a valid destination "{destination}"')
def search_for_destination(context, destination):

    # Create the SearchPage object.
    search = SearchPage(context.page)

    # Search for the supplied valid destination.
    search.search_valid_destination(destination)


@then("the Europe destination list should be displayed")
def verify_europe_destination_list(context):

    # Verify that the destination results URL is displayed.
    assert "tripsavailable" in context.page.url, (
        "Destination results page was not opened"
    )

    # Verify that the results are for Europe.
    assert "r=Europe" in context.page.url, (
        "Europe destination results were not displayed"
    )


@when('I search for an invalid destination "{destination}"')
def search_for_invalid_destination(context, destination):

    # Create the SearchPage object.
    search = SearchPage(context.page)

    # Search for the supplied invalid destination.
    search.search_invalid_destination(destination)


@then("the no results message should be displayed")
def verify_no_results_message(context):

    # Create the SearchPage object.
    search = SearchPage(context.page)

    # Verify that the invalid search query is present in the URL.
    assert "q=XYZ12345" in context.page.url, (
        "Invalid search URL was not displayed"
    )

    # Verify that the no-results message is visible.
    assert search.is_no_results_message_displayed(), (
        "Expected no-results message was not displayed"
    )


@when('I enter a partial destination "{destination}"')
def enter_partial_destination(context, destination):

    # Create the SearchPage object.
    search = SearchPage(context.page)

    # Enter the partial destination and check suggestions.
    search.search_partial_destination(destination)


@then("Europe should appear in destination suggestions")
def verify_partial_destination_suggestion(context):

    # Create the SearchPage object.
    search = SearchPage(context.page)

    # Verify that Europe appears in the suggestions.
    assert search.is_europe_suggestion_displayed(), (
        "Europe suggestion was not displayed"
    )


# =====================================================
# TC10 - INTENTIONAL FAILURE DEMONSTRATION
# =====================================================

@then("an intentional test failure should be reported")
def intentional_test_failure(context):

    # This assertion is intentionally incorrect.
    # It demonstrates how Behave reports a failed test.
    assert False, (
        "TC10 intentional failure: "
        "This test is designed to demonstrate failure reporting."
    )


# =====================================================
# TC11 - LOGIN VALIDATION TEST STEPS
# =====================================================

@given("the GCT login page is opened")
def open_gct_login_page(context):

    # Create the LoginPage object.
    context.login = LoginPage(context.page)

    # Navigate to the GCT login page.
    context.login.open_login_page()


@when("I enter invalid login credentials")
def enter_invalid_login_credentials(context):

    # Enter an invalid username.
    context.login.enter_username("thrinethra")

    # Enter a dummy password.
    context.login.enter_password("Dummy123!")


@when("I click the login submit button")
def click_login_submit(context):

    # Submit the login form.
    context.login.click_submit()


@then("an appropriate login error message should be displayed")
def verify_login_error(context):

    # Verify that the expected login error appears.
    assert context.login.is_login_error_displayed(), (
        "Expected login error message was not displayed"
    )


# =====================================================
# TC12 - REGISTRATION LOOKUP VALIDATION
# =====================================================

@given("the GCT registration lookup page is opened")
def open_registration_lookup_page(context):

    # Create the SignupPage object using the current browser page.
    context.signup = SignupPage(context.page)

    # Navigate to the registration lookup page.
    context.signup.open_registration_lookup_page()


@then("the email required validation message should be displayed")
def verify_email_required_message(context):

    # Check whether the email required message is visible.
    context.signup.verify_email_required_error()


@then("the Enter button should be disabled")
def verify_enter_button_disabled(context):

    # Check whether the Enter button is disabled.
    context.signup.verify_enter_button_disabled()


# =====================================================
# TC13 - SPECIAL OFFERS PAGE
# =====================================================

@given("the GCT homepage is opened for Special Offers")
def open_homepage_for_special_offers(context):

    # Create the HomePage Page Object.
    context.home = HomePage(context.page)

    # Open the GCT homepage.
    context.home.open_homepage()

    print("GCT homepage opened successfully!")


@when("I click the Special Offers navigation link")
def click_special_offers_navigation(context):

    # Use the HomePage method to navigate to Special Offers.
    # Popup handling and URL verification are managed inside the Page Object.
    context.home.open_special_offers()

    # Create the SpecialOffersPage object after navigation.
    context.special_offers = SpecialOffersPage(context.page)

    print("Special Offers navigation completed!")


@then("the Special Offers page should load successfully")
def verify_special_offers_page(context):

    # Verify the URL and main page content.
    context.special_offers.verify_special_offers_page()


# =====================================================
# TC14 - ORIGINAL AND DISCOUNTED PRICES
# =====================================================

@then("the original and discounted prices should be displayed")
def verify_original_and_discounted_prices(context):

    # Call the TC14 method from the Special Offers Page Object.
    context.special_offers.verify_original_and_discounted_prices()


# =====================================================
# TC15 - OFFER DETAILS NAVIGATION
# =====================================================

@when("I click the first offer details link")
def click_first_offer_details(context):

    # Call the click method from the Special Offers Page Object.
    context.special_offers.click_first_offer_details()


@then("the offer trip details page should be displayed")
def verify_offer_trip_details_page(context):

    # Call the verification method from the Page Object.
    context.special_offers.verify_offer_trip_details_page()


# =====================================================
# TC16 - RIVERS OF EUROPE NAVIGATION
# =====================================================

@given("the GCT homepage is opened for River Europe")
def open_homepage_for_river_europe(context):

    # Create the HomePage object.
    context.home = HomePage(context.page)

    # Open the GCT homepage.
    context.home.open_homepage()

    # Accept cookies if the cookie popup appears.
    context.home.accept_cookies()

    # Close the Black Friday promotional popup.
    context.home.close_promo_popup()

    print("GCT homepage opened for River Europe!")


@when("I click the Rivers of Europe tab")
def click_rivers_of_europe_tab(context):

    # Create the RiverEuropePage object.
    context.river_europe = RiverEuropePage(context.page)

    # Click the Rivers of Europe tab.
    context.river_europe.click_rivers_of_europe_tab()


@then("the River Europe cruises should be displayed")
def verify_river_europe_cruises(context):

    # Verify that River Europe cruises are displayed.
    context.river_europe.verify_river_cruises_displayed()


# =====================================================
# TC17 - HOLLAND AND BELGIUM CRUISE SELECTION
# =====================================================

@when("I click the Holland and Belgium cruise")
def click_holland_belgium_cruise(context):

    # Click the Holland and Belgium cruise.
    context.river_europe.click_holland_belgium_cruise()


@then("the Holland and Belgium cruise overview should be displayed")
def verify_holland_belgium_overview(context):

    # Verify the cruise overview page.
    context.river_europe.verify_holland_belgium_overview()


# =====================================================
# TC18 - VIEW DATES AND PRICES
# =====================================================

@when("I click the View dates and prices link")
def click_view_dates_and_prices(context):

    # Open the dates and prices page.
    context.river_europe.click_view_dates_and_prices()


@then("the Departure Details page should be displayed")
def verify_departure_details_page(context):

    # Verify the Departure Details page.
    context.river_europe.verify_departure_details_page()


# =====================================================
# TC19 - DEPARTURE DATE AND CABIN SELECTION
# =====================================================

@when("I expand March 2027 departure dates")
def expand_march_2027_dates(context):

    # Expand the March 2027 departure dates.
    context.river_europe.expand_march_2027_dates()


@when("I select the March 26 departure date")
def select_march_26_departure(context):

    # Select the March 26 - April 6, 2027 departure.
    context.river_europe.select_march_26_departure()


@then("the cabin options should be displayed")
def verify_cabin_options(context):

    # Verify that cabin options are displayed.
    context.river_europe.verify_cabin_options_displayed()


@when("I select Category C cabin")
def select_category_c_cabin(context):

    # Select Category C cabin.
    context.river_europe.select_category_c_cabin()


@when("I click Next: Trip Extensions")
def click_next_trip_extensions(context):

    # Move to the Trip Extensions stage.
    context.river_europe.click_next_trip_extensions()


# =====================================================
# TC20 - TRIP EXTENSIONS AND PRICING SUMMARY
# =====================================================

@then("the Trip Extensions stage should be displayed")
def verify_trip_extensions(context):

    # Verify that the Trip Extensions stage is displayed.
    context.river_europe.verify_trip_extensions_page()


@when("I click Next: Pricing Summary")
def click_next_pricing_summary(context):

    # Move to the Pricing Summary stage.
    context.river_europe.click_next_pricing_summary()


@then("the Pricing Summary page should be displayed")
def verify_pricing_summary(context):

    # Verify that the Pricing Summary page is displayed.
    context.river_europe.verify_pricing_summary_page()
