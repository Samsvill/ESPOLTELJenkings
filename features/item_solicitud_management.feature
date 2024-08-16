Feature: ItemSolicitud Management

  Scenario: Create an itemsolicitud with valid data
    Given I am an itemsolicitud test client
    And I have an itemsolicitud setup with valid solicitud and project
    When I send a POST request to create an itemsolicitud with valid data
    Then the response status should be 201 for itemsolicitud creation

  Scenario: Create an itemsolicitud with an invalid solicitud ID
    Given I am an itemsolicitud test client
    And I have an itemsolicitud setup with valid solicitud and project
    And I have an itemsolicitud setup with an invalid solicitud ID
    When I send a POST request to create an itemsolicitud with invalid data
    Then the response status should be 404 for itemsolicitud creation

  Scenario: Create an itemsolicitud without a token
    Given I am an itemsolicitud test client
    And I have an itemsolicitud setup with valid solicitud and project
    When I send a POST request to the itemsolicitud endpoint without a token
    Then the response status should be 401 for itemsolicitud creation
