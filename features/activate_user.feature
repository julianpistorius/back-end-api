Feature: Activate a user because user tokens are not in browser local storage.
  This could be because the user is new or the user exists but browser local storage is empty

  Background:
    Given an activation URL
    And email for persona "new_user"

  Scenario: Complete authorization with valid token
#    Given I have an activation URL with valid token
    Given I have a valid token
    When I go to the activation URL with the token
    Then I should get a 201 Created response
    And The response is valid according to the "activated_user" schema

  Scenario: Complete activation with invalid token
#    Given I have an activation URL with invalid token
    Given I have an invalid token
    When I go to the activation URL with the token
    Then I should get a 400 Bad request response to redirect to the registration page


