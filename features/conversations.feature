Feature: Get conversations, create conversations, and post responses

  Background:
    Given "group" entity
    And "marnee" user entity
    And "julian" user entity
    And "conversation" conversation entity

   Scenario: Authorized user starts conversation with another user
     Given the header contains a good x-auth-key
     When the client requests POST to start a new conversation
     Then the response is 201
     And the response is valid according to the "conversation" schema
     And "marnee" has a conversation with "julian"
     And "julian" has a conversation with "marnee"

   Scenario: Unauthorized user starts conversation with another user
     Given the header contains a bad x-auth-key
     When the client requests POST to start a new conversation
     Then the response is 401
     And no new conversation have been created

   Scenario: Authorized user responds to conversation
     Given the header contains a good x-auth-key
     When the client requests POST to respond to a conversation
     Then the response is 201
     And the response is valid according to the "response" schema
     And "conversation" has a new response
     And response is by "julian"
