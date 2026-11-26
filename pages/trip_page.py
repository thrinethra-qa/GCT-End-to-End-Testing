import time

from playwright.sync_api import expect

from pages.base_page import BasePage


class TripPage(BasePage):
    # This title was confirmed in the live Europe search results.
    DEMO_TRIP_NAME = "Rhine River: Canals, Castles & Cultural Treasures"

    def open_demo_trip(self):
        self.close_promo_popup()
        trip_link = self.page.get_by_role(
            "link",
            name=self.DEMO_TRIP_NAME,
            exact=True
        ).first
        expect(trip_link).to_be_visible(timeout=20000)
        trip_link.click()

        expect(
            self.page.get_by_role(
                "heading",
                name=self.DEMO_TRIP_NAME,
                exact=True
            )
        ).to_be_visible(timeout=20000)
        self.close_promo_popup()

    def verify_overview(self):
        expect(
            self.page.get_by_role("region", name="Overview")
        ).to_be_visible(timeout=15000)

    def play_and_pause_itinerary_video(self):
        self.close_promo_popup()
        self.page.get_by_role(
            "button",
            name="Watch Itinerary",
            exact=True
        ).click()

        video_dialog = self.page.get_by_role(
            "dialog",
            name="Trip videos"
        )
        expect(video_dialog).to_be_visible(timeout=10000)

        player = video_dialog.get_by_role(
            "region",
            name="Video Player"
        )
        video = video_dialog.locator("video")
        video.wait_for(state="attached", timeout=15000)
        self.close_promo_popup(
            wait_timeout=0,
            report_absent=False
        )

        play_button = player.get_by_role(
            "button",
            name="Play",
            exact=True
        )
        pause_button = player.get_by_role(
            "button",
            name="Pause",
            exact=True
        )

        self.close_promo_popup(
            wait_timeout=0,
            report_absent=False
        )
        start_deadline = time.monotonic() + 10
        while video.evaluate("(element) => element.paused"):
            if play_button.is_visible():
                play_button.click(timeout=1000)
                break
            if time.monotonic() >= start_deadline:
                raise AssertionError(
                    "The paused video did not expose its confirmed Play "
                    "control within 10 seconds."
                )
            self.page.wait_for_timeout(100)

        expect(video).to_have_js_property("paused", False, timeout=10000)
        expect(pause_button).to_be_visible(timeout=10000)

        start_time = video.evaluate("(element) => element.currentTime")
        target_time = start_time + 20
        playback_deadline = time.monotonic() + 60
        while video.evaluate(
            "(element) => element.currentTime"
        ) < target_time:
            if time.monotonic() >= playback_deadline:
                played_seconds = (
                    video.evaluate("(element) => element.currentTime")
                    - start_time
                )
                self._pause_video(video, pause_button)
                raise AssertionError(
                    "The itinerary video did not reach 20 seconds of "
                    "playback within 60 seconds "
                    f"({played_seconds:.2f} seconds played)."
                )

            if video.evaluate("(element) => element.paused"):
                played_seconds = (
                    video.evaluate("(element) => element.currentTime")
                    - start_time
                )
                raise AssertionError(
                    "The itinerary video paused before reaching 20 seconds "
                    f"of playback ({played_seconds:.2f} seconds played)."
                )

            self.close_promo_popup(
                wait_timeout=0,
                report_absent=False
            )
            self.page.wait_for_timeout(100)

        self._pause_video(video, pause_button)
        played_seconds = (
            video.evaluate("(element) => element.currentTime")
            - start_time
        )
        if not 19.5 <= played_seconds <= 21:
            raise AssertionError(
                "The itinerary video did not play for approximately "
                f"20 seconds before pausing ({played_seconds:.2f} seconds)."
            )

        video_dialog.get_by_role(
            "button",
            name="Close",
            exact=True
        ).click()

    def _pause_video(self, video, pause_button):
        # Video.js disables pointer events on controls while they are idle.
        expect(pause_button).to_be_visible(timeout=5000)
        pause_button.evaluate("(button) => button.click()")
        expect(video).to_have_js_property("paused", True, timeout=10000)
        self.close_promo_popup(
            wait_timeout=0,
            report_absent=False
        )

    def open_ship_details(self):
        self.close_promo_popup()
        accommodations = self.page.get_by_role(
            "region",
            name="Accommodations"
        )
        ships = accommodations.get_by_role("region", name="Ships")
        expect(ships).to_be_visible(timeout=15000)

        ship_button = ships.get_by_role("button").first
        expect(ship_button).to_be_visible(timeout=10000)
        ship_button.click()

        ship_dialog = self.page.get_by_role("dialog").first
        expect(ship_dialog).to_be_visible(timeout=10000)
        self._explore_accommodation_tabs(ship_dialog)

    @staticmethod
    def _explore_accommodation_tabs(dialog):
        for tab_name in ("Overview", "Deck Plan & Cabins", "360° View"):
            tab = dialog.get_by_role("tab", name=tab_name, exact=True)
            expect(tab).to_be_visible(timeout=10000)
            tab.click()
            expect(tab).to_have_attribute("aria-selected", "true")

        dialog.get_by_role("button", name="Close", exact=True).click()
