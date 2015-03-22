Feature: Get conversations, create conversations, and post responses

  Background:
    Given start conversation group entity
    And start conversation user entity
    And conversation with user entity
    And "conversation" conversation entity
    And route to user conversation resource

   Scenario: Authorized user starts conversation with another user
     Given the request to POST a conversation contains a good x-auth-key
     When the client requests POST to start a new conversation
     Then the response to starting a conversation is 201
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
