Feature: Solicitud management

  Scenario: Create a solicitud with valid project ID
    Given I am an authenticated user with a valid token
    When I send a POST request to create a solicitud with valid data
    Then the response status should be 201

  Scenario: Create a solicitud with an invalid project ID
    Given I am an authenticated user with a valid token
    When I send a POST request to create a solicitud with an invalid project ID
    Then the response status should be 404

  Scenario: Update a solicitud with an invalid cotizacion ID
    Given I am an authenticated user with a valid token
    And I have an existing solicitud with the ID 1
    When I send a PUT request to update the solicitud with an invalid cotizacion ID
    Then the response status should be 404

  Scenario: Create a solicitud without a token
    Given I am an unauthenticated user
    When I send a POST request to create a solicitud
    Then the response status should be 401
