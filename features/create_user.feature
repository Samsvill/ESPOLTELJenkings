Feature: User Management

  Scenario: Create a user with valid data
    Given I am a test client
    And I have the registration endpoint
    When I send a POST request to create a user with valid data
    Then the response status should be 201 for user creation

  Scenario: Create a user with an existing username
    Given I am a test client
    And A user already exists with the username "lcanarte"
    And I have the registration endpoint
    When I send a POST request to create a user with the same username
    Then the response status should be 400 for user creation

  Scenario: Obtain a token with valid credentials
    Given I am a test client
    And A user exists with the username "lcanarte" and password "Jq23%aS@"
    And I have the token obtain endpoint
    When I send a POST request to obtain a token with valid credentials
    Then the response status should be 200 for token obtainment

  Scenario: Obtain a token with invalid credentials
    Given I am a test client
    And A user exists with the username "lcanarte" and password "Jq23%aS@"
    And I have the token obtain endpoint
    When I send a POST request to obtain a token with invalid credentials
    Then the response status should be 401 for token obtainment
