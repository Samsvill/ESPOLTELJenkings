Feature: Budget Item Management

  Scenario: Create a budget item successfully
    Given I am an authenticated user with a valid token for budget item management
    And I have a project with ID 1
    When I send a POST request to create a budget item with valid data
    Then the response status should be 201 for budget item

  Scenario: Create multiple budget items successfully
    Given I am an authenticated user with a valid token for budget item management
    And I have a project with ID 1
    When I send a POST request to create multiple budget items
    Then the response status should be 201 for budget item

  Scenario: Create a budget item with an invalid project ID
    Given I am an authenticated user with a valid token for budget item management
    When I send a POST request to create a budget item with an invalid project ID
    Then the response status should be 404 for budget item

  Scenario: Create a budget item without a name
    Given I am an authenticated user with a valid token for budget item management
    And I have a project with ID 1
    When I send a POST request to create a budget item without a name
    Then the response status should be 400 for budget item

  Scenario: Create a budget item without a token
    Given I have a project with ID 1
    When I send a POST request to create a budget item without a token
    Then the response status should be 401 for budget item
