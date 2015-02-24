Feature: Create interests and link them to users, groups, organizations, goals

  Background:
    Given interest entity from persona "interest"
#    Given user persona "marnee"
#    And group persona "group"
#    And organization persona "organization"
#    And goal persona "goal"
#    And interest persona "interest"

  Scenario: Create interests for user entity
    Given entity persona "marnee"
    And route to entity
    When the client requests POST to entity route with the body:
    """
    {
        "interests": [
            {
                "name": "Ketogenic Diet",
                "description": "How to follow a ketogenic diet",
                "experience": "Trying to start a ketogenic diet",
                "time": "2 weeks"
            }
        ]
    }
    """
    Then the response is 201 created status code
    And the "interest" is created and linked to the entity

  Scenario: Create interests for group entity
    Given entity persona "group"
    And route to entity
    When the client requests POST to entity route with the body:
    """
    {
        "interests": [
            {
                "name": "Ketogenic Diet",
                "description": "How to follow a ketogenic diet",
                "experience": "Trying to start a ketogenic diet",
                "time": "2 weeks"
            }
        ]
    }
    """
    Then the response is 201 created status code
    And the "interest" is created and linked to the entity

