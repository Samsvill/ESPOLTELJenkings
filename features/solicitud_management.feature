Feature: Solicitud Management

  Scenario: Create a solicitud with valid data
    Given I am a solicitudes test client
    And I have a valid user setup with solicitud role
    When I send a POST request to create a solicitud with valid data
    Then the response status should be 201 for solicitud creation

  Scenario: Create a solicitud with an invalid project ID
    Given I am a solicitudes test client
    And I have a valid user setup with solicitud role
    And I have a solicitud setup with an invalid project ID
    When I send a POST request to create a solicitud with invalid data
    Then the response status should be 404 for solicitud creation

  Scenario: Update a solicitud with an invalid cotizacion ID
    Given I am a solicitudes test client
    And I have a valid user setup with solicitud role
    And I have a solicitud setup with valid project and estado
    And I have a cotizacion setup with a non-existing ID
    When I send a PUT request to update the solicitud with an invalid cotizacion ID
    Then the response status should be 404 for solicitud update_estado

  Scenario: Create a solicitud without a token
    Given I am a solicitudes test client
    And I have a valid user setup with solicitud role
    When I send a POST request to create a solicitud without a token
    Then the response status should be 401 for solicitud creation

  Scenario: Update the estado of a solicitud with valid IDs
    Given I am a solicitudes test client
    And I have a valid user setup with solicitud role
    And I have a solicitud setup with valid project and estado
    When I send a PUT request to update the estado of a solicitud with valid IDs
    Then the response status should be 200 for solicitud update_estado

  Scenario: Update the estado of a solicitud with invalid IDs
    Given I am a solicitudes test client
    And I have a valid user setup with solicitud role
    And I have a solicitud setup with valid project and estado
    And I have a solicitud setup with an invalid project ID
    When I send a PUT request to update the estado of a solicitud with invalid IDs
    Then the response status should be 404 for solicitud update_estado

  Scenario: Update the estado of a solicitud without a token
    Given I am a solicitudes test client
    And I have a valid user setup with solicitud role
    And I have a solicitud setup with valid project and estado
    When I send a PUT request to update the estado of a solicitud without a token
    Then the response status should be 401 for solicitud update_estado
