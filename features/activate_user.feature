Feature: Activate a user because user tokens are not in browser local storage.
  This could be because the user is new or the user exists but browser local storage is empty

  Background:
    Given an activation URL
    And email for persona "new_user"

  Scenario: Complete authorization with valid token
#    Given I have an activation URL with valid token
    Given URL payload is valid
    When Client POST to "/users/activation" with body:
    """
    {
      "user": {
          "email": "email@example.com",
          "payload": "dlgkdshgflkghsdlfkghfdlkghdflkghfgh"
      }
    }
    """
    Then The response should be HTTP 201 Created
    And The response is valid according to the "activated_user" schema

  Scenario: Complete activation with invalid token
#    Given I have an activation URL with invalid token
    Given URL payload is invalid
    When Client POST to "/users/activation" with body:
    """
    {
      "user": {
          "email": "email@example.com",
          "payload": "dlgkdshgflkghsdlfkghfdlkghdflkghfgh"
      }
    }
    """
    Then The response should be 400 Bad request


