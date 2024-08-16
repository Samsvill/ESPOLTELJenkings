Feature: Project Management

  Scenario: Create a project with valid data
    Given I am a proyecto test client
    And I have a valid user setup with project role
    When I send a POST request to create a project with valid data
    Then the response status should be 201 for project creation

  Scenario: Create a project with an existing name
    Given I am a proyecto test client
    And I have a valid user setup with project role
    And I have a project setup with an existing name
    When I send a POST request to create a project with existing_name data
    Then the response status should be 400 for project creation

  Scenario: Create a project without a token
    Given I am a proyecto test client
    And I have a valid user setup with project role
    When I send a POST request to create a project without a token
    Then the response status should be 401 for project creation

  Scenario: Update a project with valid data
    Given I am a proyecto test client
    And I have a valid user setup with project role
    When I send a PUT request to update a project with valid data
    Then the response status should be 200 for project update

  Scenario: Update a project with an invalid ID
    Given I am a proyecto test client
    And I have a valid user setup with project role
    When I send a PUT request to update a project with invalid_id data
    Then the response status should be 404 for project update
