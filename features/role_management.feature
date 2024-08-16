Feature: Role Management

  Scenario: Create a role with valid data
    Given I am a roles test client
    And I have a valid user setup for roles
    When I send a POST request to create a role with valid data
    Then the response status should be 201 for role creation

  Scenario: Delete an existing role
    Given I am a roles test client
    And I have a valid user setup for roles
    And I have a role setup with an existing role
    When I send a DELETE request to delete an existing role
    Then the response status should be 204 for role deletion

  Scenario: Delete a non-existing role
    Given I am a roles test client
    And I have a valid user setup for roles
    When I send a DELETE request to delete a non-existing role
    Then the response status should be 404 for role deletion
