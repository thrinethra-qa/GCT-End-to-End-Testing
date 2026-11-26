
Feature: GCT Client Demo Journey

  Scenario: Add a Europe trip to My Account
    Given the GCT login page is opened with consent and promotions handled
    When I log in with the configured GCT credentials
    And I search for Europe from Find Your Trip
    And I open the Europe demo trip
    Then I explore the overview and pause the itinerary video after 20 seconds
    When I explore the available ship accommodation tabs
    And I select a 2027 departure date and cabin
    And I continue to Pricing Summary
    And I decline travel protection and save the pricing summary
    Then the trip is visible in View My Account
    When I log out of My Account
    Then I am returned to the GCT login page
