Feature: Cotizacion Management

  Scenario: Create a cotizacion with valid data
    Given I am an authenticated user with a valid token for cotizacion management
    And I have a valid solicitud and project setup
    When I send a POST request to create a cotizacion with valid data
    Then the response status should be 201 for cotizacion

  Scenario: Create a cotizacion with an invalid solicitud ID
    Given I am an authenticated user with a valid token for cotizacion management
    When I send a POST request to create a cotizacion with an invalid solicitud ID
    Then the response status should be 404 for cotizacion

  Scenario: Create a cotizacion without a token
    Given I am an authenticated user with a valid token for cotizacion management
    And I have a valid solicitud and project setup
    When I send a POST request to create a cotizacion without a token
    Then the response status should be 401 for cotizacion

  Scenario: Delete a cotizacion with a valid solicitud ID
    Given I am an authenticated user with a valid token for cotizacion management
    And I have a valid solicitud and project setup
    When I send a DELETE request to delete a cotizacion with a valid solicitud ID
    Then the response status should be 200 for delete cotizacion

  Scenario: Delete a cotizacion with an invalid solicitud ID
    Given I am an authenticated user with a valid token for cotizacion management
    When I send a DELETE request to delete a cotizacion with an invalid solicitud ID
    Then the response status should be 404 for delete cotizacion

  Scenario: Delete a cotizacion without a token
    Given I am an authenticated user with a valid token for cotizacion management
    And I have a valid solicitud and project setup
    When I send a DELETE request to delete a cotizacion without a token
    Then the response status should be 401 for delete cotizacion
