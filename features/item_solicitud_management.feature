Feature: Item Solicitud management

  Scenario: Create an item solicitud with a valid solicitud ID
    Given I am an authenticated user with a valid token
    When I send a POST request to create an item solicitud with valid data
    Then the response status should be 201

  Scenario: Create an item solicitud with an invalid solicitud ID
    Given I am an authenticated user with a valid token
    When I send a POST request to create an item solicitud with an invalid solicitud ID
    Then the response status should be 404

  Scenario: Create an item solicitud without a token
    Given I am an unauthenticated user
    When I send a POST request to create an item solicitud
    Then the response status should be 401
