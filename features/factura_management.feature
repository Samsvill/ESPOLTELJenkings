Feature: Factura Management

  Scenario: Create a factura with valid data
    Given I am a factura test client
    And I have a factura setup with valid solicitud and project
    When I send a POST request to create a factura with valid data
    Then the response status should be 201 for factura creation

  Scenario: Create a factura with an invalid solicitud ID
    Given I am a factura test client
    And I have a factura setup with valid solicitud and project
    And I have a factura setup with an invalid solicitud ID
    When I send a POST request to create a factura with invalid data
    Then the response status should be 404 for factura creation

  Scenario: Create a factura without a token
    Given I am a factura test client
    And I have a factura setup with valid solicitud and project
    When I send a POST request to the factura endpoint without a token
    Then the response status should be 401 for factura creation

  Scenario: Update a factura with valid data
    Given I am a factura test client
    And I have a factura setup with valid solicitud and project
    And I have an existing factura setup
    When I send a PUT request to update the factura with valid data
    Then the response status should be 200 for factura update

  Scenario: Update a factura with an invalid solicitud ID
    Given I am a factura test client
    And I have a factura setup with valid solicitud and project
    And I have a factura setup with an invalid solicitud ID
    When I send a PUT request to update the factura with invalid data
    Then the response status should be 404 for factura update

  Scenario: Update a factura without a token
    Given I am a factura test client
    And I have a factura setup with valid solicitud and project
    And I have an existing factura setup
    When I send a PUT request to the factura endpoint without a token
    Then the response status should be 401 for factura update
