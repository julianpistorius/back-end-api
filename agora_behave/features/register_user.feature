Feature: register user
  If user wants access to all features he will need to register with the site first

  Scenario: user registers
    Given user email does not exist
    When user registers
    Then user should be created
    And temporary web token is added to user
    And user is sent an email with url to complete registration

