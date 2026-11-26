# GCT Playwright Customer Demo

This project contains one continuous Behave scenario for the GCT QA site. It
uses Python, Playwright, Chromium, page objects, and Allure. The current public
trip is **Rhine River: Canals, Castles & Cultural Treasures**.

## Requirements

- Windows PowerShell
- Python 3.10 or later
- Playwright Chromium
- Allure Commandline and Java 11+ to generate an HTML report
- An authorized GCT QA account for authenticated steps

## Setup

Run these commands from the project folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium
```

Set credentials in the current PowerShell session. The password prompt is
masked; do not put credentials in files or commands:

```powershell
$env:GCT_USERNAME = Read-Host "GCT username"
$securePassword = Read-Host "GCT password" -AsSecureString
$env:GCT_PASSWORD = (New-Object System.Net.NetworkCredential("", $securePassword)).Password
```

The code never prints either value. Playwright verifies each field matches its
environment value without printing or attaching that value. Tracing is stopped
before credential entry and resumed after successful login without screenshots
or DOM snapshots. Failure screenshots mask both login fields.
If login verification fails, its diagnostic reports first-party POST status
codes, whether exact raw environment values appeared in an inspectable
request body, and whether Submit is still loading. A false raw-password match
may mean the site transformed it; it does not prove the configured password is
wrong. Request bodies and credential values are never logged or saved.

## Run

```powershell
.\run_tests.bat
```

The run writes Allure results to `allure-results-demo\`, failure screenshots
to `screenshots\`, browser videos to `videos\`, and Playwright traces to
`traces\`.

Open a trace in Playwright Trace Viewer:

```powershell
playwright show-trace traces\<trace-file-name>.zip
```

Generate and view the Allure report:

```powershell
allure generate allure-results-demo --clean -o allure-report
allure open allure-report
```

## Current site gaps

The latest saved run reached Pricing Summary but displayed a **Save Your Trip**
dialog prompting sign-in to My Account, so authentication was not confirmed.
A missing `re` import had caused the Welcome-text check to be swallowed; the
import and error propagation are now fixed. Rerun to verify login before
investigating account navigation.

The current Rhine trip displays Ships but no Hotel section and proceeds from
cabin selection directly to Pricing Summary, not Trip Extensions. See
[LOCATORS_REQUIRED.md](LOCATORS_REQUIRED.md) for missing UI controls and the
evidence needed to add them safely.

The video opens through the confirmed **Watch Itinerary** control. Its
accessible player exposes **Play** and **Pause** controls. The scenario waits
until 20 seconds of media time have played (using Play only if the player is
paused), clicks the actual Pause control, verifies the paused state, and checks
that the video's playback time advanced for approximately 20 seconds. A
60-second load/playback limit prevents an unavailable stream from hanging the
scenario.
In an earlier public-site check, the player remained at `currentTime=0` and
`readyState=0` while reporting that it was playing. A later timed run loaded
the video after buffering and reached only 8.25 seconds of media time in 20
wall-clock seconds. The scenario waits for actual media progress and will
report a failure rather than treating a button-state change as playback. The
latest live check at the configured 1920×1080 viewport completed 20 seconds
of media playback and verified that the actual Pause control stopped it.

The Behave workflow reads `GCT_USERNAME` and `GCT_PASSWORD` from GitHub Actions
secrets. Configure those secrets before expecting an authenticated CI run.
