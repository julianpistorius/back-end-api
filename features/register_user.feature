Feature: Register new user or login existing users

  Scenario: Register new user
    Given the user is new user with persona "new_user"
    When the client requests POST to route "/users" with the body:
    """
      {
        "user": {
          "email": "email@example.com"
        }
      }
    """
    Then the response code is 201 Created

  Scenario: Activate existing user
    Given the user is existing user with persona "marnee"
    When the client requests POST to route "/users" with the body:
    """
      {
        "user": {
          "email": "marnee@agorasociety.com"
        }
      }
    """
    Then the response code is 201 Created
