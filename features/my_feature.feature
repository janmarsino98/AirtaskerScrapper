Feature: Scrape Airtasker tasks
  As a bot user
  I want to connect to an Australian VPN, load cookies, and scrape tasks on Airtasker
  So that I can analyze tasks without manual intervention

  Scenario: Valid VPN connection to Australia
    Given I have created a Chrome driver instance
    When I connect to a VPN in Australia
    Then I should verify that my VPN connection is valid

  Scenario: Load the Airtasker landing page and add cookies
    Given I have a valid VPN connection to Australia
    And I have created a Chrome driver instance
    When I navigate to the Airtasker landing page
    And I add the authentication cookies
    Then I should see the Airtasker tasks page loaded

  Scenario: Filter for only remote tasks
    Given I am on the Airtasker tasks page
    When I filter to show only remote tasks
    Then only remote tasks should be shown in the results
