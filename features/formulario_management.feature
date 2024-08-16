Feature: Formulario Management

  Scenario: Create a formulario with valid data
    Given I am a formulario test client
    And I have a formulario setup with valid solicitud and project
    When I send a POST request to create a formulario with valid data
    Then the response status should be 201 for formulario creation

  Scenario: Create a formulario with an invalid solicitud ID
    Given I am a formulario test client
    And I have a formulario setup with valid solicitud and project
    And I have a formulario setup with an invalid solicitud ID
    When I send a POST request to create a formulario with invalid data
    Then the response status should be 404 for formulario creation

  Scenario: Create a formulario without a token
    Given I am a formulario test client
    And I have a formulario setup with valid solicitud and project
    When I send a POST request to the formulario endpoint without a token
    Then the response status should be 401 for formulario creation
