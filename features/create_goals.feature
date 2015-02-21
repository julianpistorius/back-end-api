Feature: Users can create goals and associate them with their relevant interests

  Scenario: User creates a goal with interests
    Given I am a registered user with a valid permanent web token
    When I POST to URL "/users/{user_id}/goals" with the body:
    """
    {
        "goal": {
            "title": "Title Me",
            "description": "Description of goal",
            "start_date": "11/29/2014",
            "end_date": "12/29/2014",
            "is_public": "True",
            "achieved": "False",
            "interests": [
                {
                    "id": "12324355345"
                },
                {
                    "id": "0987405735"
                }
            ]
        }
    }
    """
    Then I should get a 201 Created status code
    And The response is valid according to the "users" schema
