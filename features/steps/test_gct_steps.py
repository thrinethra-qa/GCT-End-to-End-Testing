
import os

from behave import given, when, then

from pages.account_page import AccountPage
from pages.booking_page import BookingPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.trip_page import TripPage


@given("the GCT login page is opened with consent and promotions handled")
def open_gct_login_page(context):

    context.login = LoginPage(context.page)
    context.login.open_login_page()


@when("I log in with the configured GCT credentials")
def login_with_valid_credentials(context):

    # Read credentials from environment variables.
    username = os.getenv("GCT_USERNAME")
    password = os.getenv("GCT_PASSWORD")

    # Ensure both environment variables exist.
    assert username, (
        "GCT_USERNAME environment variable is not configured."
    )

    assert password, (
        "GCT_PASSWORD environment variable is not configured."
    )

    # Save the pre-login trace before submitting credentials.
    # This avoids storing credential-related browser snapshots.
    pre_login_trace = (
        context.trace_dir
        / f"{context.safe_scenario_name}-pre-login.zip"
    )

    if getattr(context, "tracing_started", False):

        context.browser_context.tracing.stop(
            path=str(pre_login_trace)
        )

        context.tracing_started = False

    # Perform login.
    context.login.login_with_valid_credentials(
        username,
        password
    )

    # Verify successful authentication.
    context.login.verify_successful_login()

    # Close any delayed promotional popup.
    context.login.close_promo_popup()

    # Resume tracing without screenshots or DOM snapshots.
    context.browser_context.tracing.start(
        screenshots=False,
        snapshots=False,
        sources=False
    )

    context.tracing_started = True


@when("I search for Europe from Find Your Trip")
def search_for_europe(context):

    context.home = HomePage(context.page)
    context.home.open_homepage()
    context.home.search_for_europe()


@when("I open the Europe demo trip")
def open_europe_demo_trip(context):

    context.trip = TripPage(context.page)
    context.trip.open_demo_trip()


@then(
    "I explore the overview and pause the itinerary video after 20 seconds"
)
def explore_overview_and_video(context):

    context.trip.verify_overview()
    context.trip.play_and_pause_itinerary_video()


@when("I explore the available ship accommodation tabs")
def explore_accommodations(context):

    context.trip.open_ship_details()


@when("I select a 2027 departure date and cabin")
def select_departure_and_cabin(context):

    context.booking = BookingPage(context.page)

    context.booking.open_dates_and_prices()
    context.booking.select_departure_year("2027")
    context.booking.select_departure_date()
    context.booking.select_cabin()


@when("I continue to Pricing Summary")
def continue_to_pricing_summary(context):

    context.booking.continue_to_pricing_summary()


@when(
    "I decline travel protection and save the pricing summary"
)
def save_pricing_summary(context):

    context.booking.select_no_travel_protection()
    context.booking.save_pricing_summary()


@then("the trip is visible in View My Account")
def verify_trip_in_account(context):

    context.account = AccountPage(context.page)

    context.account.open_my_account()

    context.account.verify_trip_is_added(
        TripPage.DEMO_TRIP_NAME
    )


@when("I log out of My Account")
def log_out_of_account(context):

    context.account.log_out()


@then("I am returned to the GCT login page")
def verify_logged_out(context):

    context.account.verify_logged_out()
