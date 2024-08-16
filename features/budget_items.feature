Feature: Budget item management

  Scenario: Create a budget item with a valid project ID
    Given I am an authenticated user with a valid token
    When I send a POST request to create a budget item with valid data
    Then the response status should be 201

  Scenario: Create multiple budget items with a valid project ID
    Given I am an authenticated user with a valid token
    When I send a POST request to create multiple budget items
    Then the response status should be 201

  Scenario: Create a budget item with an invalid project ID
    Given I am an authenticated user with a valid token
    When I send a POST request to create a budget item with an invalid project ID
    Then the response status should be 404

  Scenario: Create a budget item with no name provided
    Given I am an authenticated user with a valid token
    When I send a POST request to create a budget item without a name
    Then the response status should be 400

  Scenario: Create a budget item without a token
    Given I am an unauthenticated user
    When I send a POST request to create a budget item
    Then the response status should be 401
