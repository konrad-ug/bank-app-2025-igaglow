Feature: Account registry

  Background:
    Given Account registry is empty

  Scenario: User is able to create 2 accounts
    When I create an account using name: "kurt", last name: "cobain", pesel: "89092909246"
    And I create an account using name: "tadeusz", last name: "szcześniak", pesel: "79101011234"
    Then Number of accounts in registry equals: "2"
    And Account with pesel "89092909246" exists in registry
    And Account with pesel "79101011234" exists in registry

  Scenario: User is able to update surname of already created account
    And I create an account using name: "nata", last name: "haydamaky", pesel: "95092909876"
    When I update "surname" of account with pesel: "95092909876" to "filatov"
    Then Account with pesel "95092909876" has "surname" equal to "filatov"

  Scenario: User is able to update name of already created account
    And I create an account using name: "jan", last name: "kowalski", pesel: "11111111111"
    When I update "name" of account with pesel: "11111111111" to "adam"
    Then Account with pesel "11111111111" has "name" equal to "adam"

  Scenario: Created account has all fields correctly set
    When I create an account using name: "robert", last name: "maklowicz", pesel: "52081200123"
    Then Account with pesel "52081200123" has "name" equal to "robert"
    And Account with pesel "52081200123" has "surname" equal to "maklowicz"
    And Account with pesel "52081200123" has "balance" equal to "0"

  Scenario: User is able to delete created account
    And I create an account using name: "parov", last name: "stelar", pesel: "01092909876"
    When I delete account with pesel: "01092909876"
    Then Account with pesel "01092909876" does not exist in registry
    And Number of accounts in registry equals: "0"

  Scenario: User is able to perform incoming transfer
    And I create an account using name: "bill", last name: "gates", pesel: "55050512345"
    When I perform "incoming" transfer to account with pesel: "55050512345" for amount: "100.50"
    Then Account with pesel "55050512345" has balance equal to "100.50"

  Scenario: Persisting accounts in database
    Given Account registry is empty
    And I create an account using name: "Jan", last name: "Kowalski", pesel: "11111111111"
    When I save accounts to database
    And Account registry is empty
    And I load accounts from database
    Then Number of accounts in registry equals: "1"
    And Account with pesel "11111111111" exists in registry