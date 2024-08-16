Feature: Project management

  Scenario: Create a new project
    Given I am an authenticated user with a valid token
    When I send a POST request to create a new project with valid data
    Then the response status should be 201

  Scenario: Create a project with an existing name
    Given I am an authenticated user with a valid token
    And I have an existing project with the name "Proyecto prueba"
    When I send a POST request to create a project with the same name
    Then the response status should be 400

  Scenario: Create a project without a token
    Given I am an unauthenticated user
    When I send a POST request to create a new project
    Then the response status should be 401

  Scenario: Update a project with a valid ID
    Given I am an authenticated user with a valid token
    And I have an existing project with the ID 1
    When I send a PUT request to update the project
    Then the response status should be 200

  Scenario: Update a project with an invalid ID
    Given I am an authenticated user with a valid token
    And there is no project with ID 100
    When I send a PUT request to update the project
    Then the response status should be 404
