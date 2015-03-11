Feature: Get users, interests, and groups by name.  Matches on the search string.  May return more than one
  result

  Scenario: Get user by name
    Given search string "Mar"
    And route to entity search
    When the client requests GET from entity route with parameters
    Then the response is 200
    And the response is valid according to the "entity_search_results" schema

  Scenario: Get group by name
    Given search string "Tuc"
    And route to entity search
    When the client requests GET from entity route with parameters
    Then the response is 200
    And the response is valid according to the "entity_search_results" schema

  Scenario: Get interest by name
    Given search string "ket"
    And route to entity search
    When the client requests GET from entity route with parameters
    Then the response is 200
    And the response is valid according to the "entity_search_results" schema