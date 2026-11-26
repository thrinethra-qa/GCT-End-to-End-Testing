@echo off
setlocal

if not exist allure-results-demo mkdir allure-results-demo

python -m behave features\gct_tests.feature ^
  --format allure_behave.formatter:AllureFormatter ^
  --outfile allure-results-demo ^
  --no-capture

set "TEST_EXIT_CODE=%ERRORLEVEL%"
if not "%TEST_EXIT_CODE%"=="0" (
  echo Behave demo failed. Review the terminal output and saved evidence.
)

exit /b %TEST_EXIT_CODE%
