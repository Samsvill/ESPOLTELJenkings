Feature: Cotizacion management

  Scenario: Create a cotizacion with valid solicitud ID
    Given I am an authenticated user with a valid token
    When I send a POST request to create a cotizacion with valid data
    Then the response status should be 201

  Scenario: Create a cotizacion with an invalid solicitud ID
    Given I am an authenticated user with a valid token
    When I send a POST request to create a cotizacion with an invalid solicitud ID
    Then the response status should be 404

  Scenario: Create a cotizacion without a token
    Given I am an unauthenticated user
    When I send a POST request to create a cotizacion
    Then the response status should be 401

  Scenario: Delete a cotizacion with a valid solicitud ID
    Given I am an authenticated user with a valid token
    When I send a DELETE request to delete a cotizacion with a valid solicitud ID
    Then the response status should be 200

  Scenario: Delete a cotizacion with an invalid solicitud ID
    Given I am an authenticated user with a valid token
    When I send a DELETE request to delete a cotizacion with an invalid solicitud ID
    Then the response status should be 404

  Scenario: Delete a cotizacion without a token
    Given I am an unauthenticated user
    When I send a DELETE request to delete a cotizacion
    Then the response status should be 401
