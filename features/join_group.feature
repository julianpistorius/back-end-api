Feature: Users can join and leave existing groups

  Background:
    Given "group" group entity
    And "marnee" user entity
    And route to join groups

  Scenario: Authorized user joins group
    Given the header contains a good x-auth-key
    When the client requests POST to join groups route
    Then the response is 201
    And the response is valid according to the "user_joined" schema
    And "marnee" is a member of "group"

  Scenario: Unauthorized user joins group
    Given the header contains a bad x-auth-key
    When the client requests POST to join groups route
    Then response is 401
    And "marnee" is not a member of "group"