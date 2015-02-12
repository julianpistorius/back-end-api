Feature: Authorize an existing user because user tokens are not in browser local storage

  Scenario: Send user authorization URL
    Given I am a registered user
    When I POST to URL "/login"
    Then I should get a 202 Accepted response

  Scenario: Complete authorization with valid token
    Given I am a registered user
    And I go to the authorization URL from my email
    And The token is valid
    Then I should get a 200 OK response
    And The response is valid according to the "authorized_user" schema

  Scenario: Complete authorization with invalid token
    Given I am a registered user
    And I got to the authorization URL
    And The token is not valid
    Then I should get a 303 See Other response to redirect to the registration page
    And The response is valid according to the "redirect" schema


