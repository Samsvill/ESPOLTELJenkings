Feature: Formulario management

  Scenario: Create a formulario with a valid solicitud ID
    Given I am an authenticated user with a valid token
    When I send a POST request to create a formulario with valid data
    Then the response status should be 201

  Scenario: Create a formulario with an invalid solicitud ID
    Given I am an authenticated user with a valid token
    When I send a POST request to create a formulario with an invalid solicitud ID
    Then the response status should be 404

  Scenario: Create a formulario without a token
    Given I am an unauthenticated user
    When I send a POST request to create a formulario
    Then the response status should be 401
