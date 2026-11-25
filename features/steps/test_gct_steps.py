
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

    # Initialize the Special Offers Page Object.
    context.special_offers = SpecialOffersPage(context.page)

    print("Special Offers Page Object initialized successfully!")


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
        "https://qa.gct.com/",
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

    # Print the actual URL currently displayed in the browser.
    print(f"\nDEBUG - Actual homepage URL: {context.page.url}")

    # Define the expected homepage URL.
    expected_url = "https://qa.gct.com/"

    # Compare the actual URL with the expected URL.
    assert context.page.url == expected_url, (
        f"GCT homepage did not load successfully. "
        f"Expected: {expected_url}, Actual: {context.page.url}"
    )

    print("Homepage loaded successfully!")

@then("I should return to the homepage")
def verify_homepage_navigation(context):

    # Print the actual URL after browser navigation.
    print(f"Actual URL after navigation: {context.page.url}")

    # Define the expected homepage URL.
    expected_url = "https://qa.gct.com/"

    # Verify that browser navigation returned to the homepage.
    assert context.page.url == expected_url, (
        f"Browser did not return to the homepage. "
        f"Expected: {expected_url}, Actual: {context.page.url}"
    )

    print("Successfully returned to the homepage!")


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


# Match the wording used in the existing feature file.
@then("the Special Offers page should be displayed")

# Keep support for the original wording as well.
@then("the Special Offers page should load successfully")
def verify_special_offers_page(context):

    # Verify that the Special Offers page is displayed.
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

# ============================================================
# EC01 - Search destination using only blank spaces
# ============================================================
@given("the user is on the GCT homepage")
def step_user_on_gct_homepage(context):

    # Create the HomePage object.
    context.home = HomePage(context.page)

    # Navigate to the GCT homepage.
    context.home.open_homepage()

    # Accept cookies if the consent dialog appears.
    context.home.accept_cookies()

    print("GCT homepage opened successfully.")
@when("the user enters only spaces in destination search")
def step_enter_spaces_only(context):

    # Create the SearchPage object using the current browser page.
    context.search = SearchPage(context.page)

    # Enter five blank spaces into the destination search field.
    context.search.search_with_spaces_only()

    print("Entered five blank spaces in destination search.")


@then("no destination autocomplete suggestions should appear")
def step_verify_no_destination_suggestions(context):

    # Check whether the autocomplete dropdown is displayed.
    suggestions_displayed = (
        context.search.are_destination_suggestions_displayed()
    )

    # The test passes only when no dropdown is displayed.
    assert not suggestions_displayed, (
        "EC01 FAILED: Destination autocomplete suggestions appeared "
        "after entering only blank spaces."
    )

    print(
        "EC01 PASSED: No destination autocomplete suggestions appeared."
    )

# ============================================================
# EC02 - Search destination using special characters
# ============================================================

@when("the user enters special characters in destination search")
def step_enter_special_characters(context):

    # Create the SearchPage object.
    context.search = SearchPage(context.page)

    # Enter special characters into the search field.
    context.search.search_with_special_characters()

    print("Entered special characters in destination search.")


@then("the destination search should handle the input without errors")
def step_verify_special_character_search(context):

    # Read the current value from the search field.
    actual_value = context.page.locator(
        "//input[@id='_R_5cn5b_']"
    ).input_value()

    # Verify that the entered characters remain in the input.
    assert actual_value == "@#$%^&*", (
        f"EC02 FAILED: Expected '@#$%^&*' but found '{actual_value}'."
    )

    print("EC02 PASSED: Special characters were accepted in the search field.")

# ============================================================
# EC03 - Search destination using an extremely long input
# ============================================================

@when("the user enters an extremely long destination")
def step_enter_long_destination(context):

    # Create the SearchPage object.
    context.search = SearchPage(context.page)

    # Enter 500 characters into the destination search.
    context.search.search_with_long_input()

    print("Entered 500 characters in destination search.")


@then("the destination search should handle the long input without errors")
def step_verify_long_destination(context):

    # Get the current value from the search input.
    actual_value = context.page.locator(
        "//input[@id='_R_5cn5b_']"
    ).input_value()

    # Verify that all 500 characters were retained.
    assert len(actual_value) == 500, (
        f"EC03 FAILED: Expected 500 characters, "
        f"but found {len(actual_value)}."
    )

    print(
        "EC03 PASSED: Search field retained all "
        f"{len(actual_value)} characters."
    )


# ============================================================
# EC04 - Login using whitespace-only credentials
# ============================================================

@when("the user enters whitespace-only credentials")
def step_enter_whitespace_credentials(context):

    # Reuse the LoginPage object created by the existing Given step.
    context.login.enter_whitespace_credentials()


@when("the user clicks the login submit button")
def step_click_login_submit(context):

    # Click the existing login Submit button.
    context.login.click_submit()


@then("the login should be prevented")
def step_verify_whitespace_login(context):

    # Verify that the user remains on the sign-in page.
    assert "/account/signin" in context.page.url.lower(), (
        "EC04 FAILED: User navigated away from the sign-in page."
    )

    print("EC04 PASSED: Login was not successful with whitespace credentials.")


# ============================================================
# EC05 - Signup with invalid email formats
# ============================================================

@given("the GCT Registration Lookup page is opened")
def step_open_registration_lookup(context):
    # Create the SignupPage object.
    context.signup = SignupPage(context.page)

    # Open the registration lookup page.
    context.signup.open_registration_lookup_page()


@when('the user enters an invalid email "{email}"')
def step_enter_invalid_email(context, email):
    # Enter the supplied invalid email address.
    context.signup.enter_email_for_validation(email)


@then("the email format should be rejected")
def step_verify_invalid_email(context):
    # Check the browser's built-in email validation.
    is_valid = context.signup.is_email_format_valid()

    # Invalid email formats should not pass validation.
    assert not is_valid, (
        f"EC05 FAILED: Email "
        f"'{context.page.locator(context.signup.email_field).input_value()}' "
        "was accepted by the browser's email validation."
    )

    print("EC05 PASSED: Invalid email format was rejected.")

# ============================================================
# EC06 - Valid-looking username with empty password
# ============================================================

@when("the user enters a valid-looking username without a password")
def step_enter_username_without_password(context):

    # Enter a test username. Leave the password field empty.
    context.login.enter_username("tester@example.com")

@then("the login submit button should be disabled")
def step_verify_login_submit_disabled(context):

    # Check whether the Submit button is disabled.
    is_disabled = context.login.submit_button.is_disabled()

    assert is_disabled, (
        "EC6 FAILED: Submit button was enabled with an empty password."
    )

    print("EC6 PASSED: Submit button is disabled when password is empty.")