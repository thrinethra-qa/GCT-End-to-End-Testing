# Locators and UI behavior still requiring confirmation

Do not guess selectors for the items below. Public inspection used the
**Rhine River: Canals, Castles & Cultural Treasures** trip. `GCT_USERNAME` and
`GCT_PASSWORD` are only read from the local environment and are not retained
in the project. The latest attempted login remained on the sign-in page, so
authenticated account steps were not run.

## Confirmed controls

- Login: `input[name='signin-username']`,
  `input[name='signin-password']`, and the Submit button.
- Europe search: Find Your Trip, Destination, Search destinations, Europe,
  Apply, and Search for trips. The Rhine trip appeared in the results.
- Video: **Watch Itinerary** opens a **Trip videos** dialog. The dialog has a
  **Video Player** region with actual **Play** and **Pause** buttons and an
  HTML video element; no video iframe was present. The code uses Play only if
  the video is paused, waits until 20 seconds of media time have played,
  clicks Pause, verifies the paused state, and checks media-time progress.
  A 60-second timeout prevents unavailable streams from hanging the scenario.
- Ship: the Accommodations section exposes Ships. The ship dialog tabs are
  **Overview**, **Deck Plan & Cabins**, and **360° View**.
- Public booking: year filter includes 2027; departure control is **Select
  Date**, cabin control is **Select Cabins**, and the observed next step is
  **Next: Pricing Summary**.
- Promotion: the `$3,000` offer appears as a **Close banner** control and can
  also appear in a **Save up to $3,000** dialog.

### Video playback

- **Observed:** The video reported `paused=false` but initially remained at
  `currentTime=0` and `readyState=0`. A later timed run loaded the stream but
  reached only 8.25 seconds of media time during 20 seconds of wall-clock time.
- **Validation:** The scenario now waits for 20 seconds of media-time progress,
  then clicks the actual Pause control; a live run at 1920×1080 passed this
  check. It fails with a bounded timeout if the stream does not load or
  advance.

## Missing or unverified requested flow

### Cookie and promotional dialogs

- **Requested:** Dismiss cookie consent, the Black Friday promotion, and the
  post-login newsletter only when visible.
- **Observed:** Cookie consent was absent in one fresh context and appeared in
  another; the **Cookie consent** dialog and **Accept** control worked. The
  `$3,000` banner/dialog was observed. A separate Black Friday modal and a
  distinct post-login newsletter were not confirmed.
- **Missing:** The separate Black Friday close control and any distinct
  post-login newsletter dialog/close control. The former `form#WebPop`
  selector was unverified and has been removed rather than used as a guessed
  locator.
- **Needed:** Inspect a clean profile and an authorized account when each
  popup appears. Do not replace these selectors with guesses.

### Hotel accommodation

- **Requested:** Explore both Ship and Hotel details.
- **Observed:** This trip exposes Ships only; no Hotel section appeared.
- **Missing:** A Europe trip with a Hotel section and confirmed Hotel card,
  open, and detail controls.
- **Needed:** Provide or confirm a suitable trip with both accommodation types.

### Trip extensions

- **Requested:** Next: Trip Extensions, extension options, and support for
  Add Trip or Find a New Departure Date.
- **Observed:** The selected trip proceeds directly to Next: Pricing Summary.
- **Missing:** A trip and departure that display Trip Extensions, plus the
  exact option names and controls.
- **Needed:** Confirm a trip/departure that supports the extensions flow.

### Authenticated account completion

- **Requested:** Save Pricing Summary, verify the trip in View My Account, and
  log out.
- **Observed:** The latest screenshot showed a `Save Your Trip` dialog
  prompting the user to sign in to My Account after Pricing Summary; the
  authenticated account was therefore not confirmed. A missing `re` import
  in the Welcome-text check has now been fixed, and verification errors are
  no longer swallowed.
- **Missing:** Confirmed authenticated account navigation, saved-trip display,
  and logout success controls.
- **Needed:** Rerun with an authorized QA account after verifying login; then
  confirm the account controls and saved-trip display. Do not put credentials
  in source files, logs, screenshots, traces, or reports.
