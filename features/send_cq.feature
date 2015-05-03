Feature: Create a cq and link to user and interests

  Background:
    Given cq entity with the body:
    """
    {
      "cq":
        {
          "subject": "BBD TEST CQ",
          "message": "BDD TEST CQ FULL MESSAGE"
        }
    }
    """
    And

  Scenario: Create CQ
    Given an authorized user
    When the client requets POST to route "/