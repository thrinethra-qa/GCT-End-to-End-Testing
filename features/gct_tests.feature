
Feature: GCT Website Testing

  @smoke
  Scenario: TC01 - Verify homepage loads successfully
    Given the GCT homepage is opened
    Then the homepage should load successfully

  @smoke
  Scenario: TC02 - Verify GCT logo navigation
    Given the GCT homepage is opened
    When I click the GCT logo
    Then I should return to the homepage

  @regression
  Scenario: TC03 - Verify Special Offers navigation
    Given the GCT homepage is opened
    When I navigate to the Special Offers page
    Then the Special Offers page should be displayed

  @regression
  Scenario: TC04 - Verify browser back navigation
    Given the GCT homepage is opened
    When I navigate to the Special Offers page
    And I click the browser back button
    Then I should return to the homepage
  

  @regression
  Scenario: TC05 - Verify browser forward navigation
    Given the GCT homepage is opened
    When I navigate to the Special Offers page
    And I click the browser back button
    And I click the browser forward button
    Then the Special Offers page should be displayed

  @regression
  Scenario: TC06 - Verify destination search field is visible and enabled
    Given the GCT homepage is opened
    Then the destination search field should be visible and enabled

  @smoke
  Scenario: TC07 - Verify valid destination search
    Given the GCT homepage is opened
    When I search for a valid destination "Europe"
    Then the Europe destination list should be displayed

  @regression
  Scenario: TC08 - Verify invalid destination search
    Given the GCT homepage is opened
    When I search for an invalid destination "XYZ12345"
    Then the no results message should be displayed

  @regression
  Scenario: TC09 - Verify partial destination suggestions
    Given the GCT homepage is opened
    When I enter a partial destination "eur"
    Then Europe should appear in destination suggestions

  @intentional_failure
  @regression
  Scenario: TC10 - Verify invalid email login validation
    Given the GCT homepage is opened
    Then an intentional test failure should be reported
  
  
  @regression @TC11
  Scenario: TC11 - Verify login with invalid username/email
    Given the GCT login page is opened
    When I enter invalid login credentials
    And I click the login submit button
    Then an appropriate login error message should be displayed


  @regression
  Scenario: TC12 - Verify registration lookup with an empty email field
    Given the GCT registration lookup page is opened
    Then the email required validation message should be displayed
    And the Enter button should be disabled

  @regression
  Scenario: TC13 - Verify Special Offers page
    Given the GCT homepage is opened for Special Offers
    When I click the Special Offers navigation link
    Then the Special Offers page should load successfully

  @regression
  Scenario: TC14 - Verify original and discounted prices are displayed
    Given the GCT homepage is opened for Special Offers
    When I click the Special Offers navigation link
    Then the original and discounted prices should be displayed

  @regression
  Scenario: TC15 - Verify offer details navigation
    Given the GCT homepage is opened for Special Offers
    When I click the Special Offers navigation link
    And I click the first offer details link
    Then the offer trip details page should be displayed

  @regression
  Scenario: TC16 - Verify Rivers of Europe navigation
    Given the GCT homepage is opened for River Europe
    When I click the Rivers of Europe tab
    Then the River Europe cruises should be displayed

  @regression
  Scenario: TC17 - Verify Holland and Belgium cruise selection
    Given the GCT homepage is opened for River Europe
    When I click the Rivers of Europe tab
    And I click the Holland and Belgium cruise
    Then the Holland and Belgium cruise overview should be displayed

  @regression
  Scenario: TC18 - Verify View dates and prices navigation
    Given the GCT homepage is opened for River Europe
    When I click the Rivers of Europe tab
    And I click the Holland and Belgium cruise
    And I click the View dates and prices link
    Then the Departure Details page should be displayed

  @regression
  Scenario: TC19 - Verify departure date and cabin selection
    Given the GCT homepage is opened for River Europe
    When I click the Rivers of Europe tab
    And I click the Holland and Belgium cruise
    And I click the View dates and prices link
    And I expand March 2027 departure dates
    And I select the March 26 departure date
    Then the cabin options should be displayed
    When I select Category C cabin
    And I click Next: Trip Extensions
    Then the Trip Extensions stage should be displayed

  @regression
  Scenario: TC20 - Verify trip extensions and pricing summary
    Given the GCT homepage is opened for River Europe
    When I click the Rivers of Europe tab
    And I click the Holland and Belgium cruise
    And I click the View dates and prices link
    And I expand March 2027 departure dates
    And I select the March 26 departure date
    And I select Category C cabin
    And I click Next: Trip Extensions
    Then the Trip Extensions stage should be displayed
    When I click Next: Pricing Summary
    Then the Pricing Summary page should be displayed

  @edge @regression
  Scenario: EC01 - Search destination using only spaces
    Given the user is on the GCT homepage
    When the user enters only spaces in destination search
    Then no destination autocomplete suggestions should appear

  @edge @regression
  Scenario: EC02 - Search destination using special characters
    Given the user is on the GCT homepage
    When the user enters special characters in destination search
    Then the destination search should handle the input without errors
  
  @edge @regression
  Scenario: EC03 - Search destination using an extremely long input
    Given the user is on the GCT homepage
    When the user enters an extremely long destination
    Then the destination search should handle the long input without errors

  @edge @regression
  Scenario: EC04 - Login using whitespace-only credentials
    Given the GCT login page is opened
    When the user enters whitespace-only credentials
    And the user clicks the login submit button
    Then the login should be prevented

  @edge @regression
  Scenario Outline: EC05 - Signup with invalid email formats
    Given the GCT Registration Lookup page is opened
    When the user enters an invalid email "<email>"
    Then the email format should be rejected

  Examples:
    | email               |
    | test@               |
    | @test.com           |
    | test user@gmail.com |

  @edge @regression
  Scenario: EC6 - Login with valid-looking username and empty password
    Given the GCT login page is opened
    When the user enters a valid-looking username without a password
    Then the login submit button should be disabled
