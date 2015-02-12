Feature: Register new user

  Background:
    Given I am a new user

  Scenario: Register new user
    Given I am a new user
    When I POST to URL "/users" with the body:
    """
      {
        "users": {
          "email": "email@example.com"
        }
      }
    """
    Then I should get a 201 Created status code
