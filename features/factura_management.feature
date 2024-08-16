Feature: Factura management

  Scenario: Create a factura with a valid solicitud ID
    Given I am an authenticated user with a valid token
    When I send a POST request to create a factura with valid data
    Then the response status should be 201

  Scenario: Create a factura with an invalid solicitud ID
    Given I am an authenticated user with a valid token
    When I send a POST request to create a factura with an invalid solicitud ID
    Then the response status should be 404

  Scenario: Create a factura without a token
    Given I am an unauthenticated user
    When I send a POST request to create a factura
    Then the response status should be 401

  Scenario: Update a factura with a valid solicitud ID
    Given I am an authenticated user with a valid token
    When I send a PUT request to update a factura with valid data
    Then the response status should be 200

  Scenario: Update a factura with an invalid solicitud ID
    Given I am an authenticated user with a valid token
    When I send a PUT request to update a factura with an invalid solicitud ID
    Then the response status should be 404

  Scenario: Update a factura without a token
    Given I am an unauthenticated user
    When I send a PUT request to update a factura
    Then the response status should be 401
