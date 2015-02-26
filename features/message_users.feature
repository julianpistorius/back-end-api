Feature: Users and group managers can send messages to other users.

  Background:
    Given "marnee"
    And "julian"

  Scenario: User wants to connect with other user and sends a message to that user.
    When the client requests POST to messaging route
    Then the response code is 201 created
    And the response is valid according to the "messages" schema
    And a message was logged

  Scenario: Group manager sends a message to group's members
    When the client requests POST to messaging route
    Then the response code is 201 created
    And the response is valid according to the "messages" schema
    And a message was logged