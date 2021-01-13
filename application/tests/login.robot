*** Settings ***

Documentation    A test suite for login functionality.
Resource         resource.robot

*** Test Cases ***

User cannot login with invalid username and password
    Given user "wrong" logs in with password "wrong"
    Then page contains "Wrong username or password"

User cannot login with a valid username and an invalid password
    Given user "kalle" registers with password "password"
    When user "kalle" logs in with password "wrong"
    Then page contains "Wrong username or password"

User can login with a valid username and password
    Given user "kalle" registers with password "password"
    When user "kalle" logs in with password "password"
    Then page contains "log out"

User can logout
    Given user "kalle" registers with password "password"
    When user "kalle" logs in with password "password"
    Then page does not contain "log in"
    When user logs out
    Then page contains "log in"

*** Keywords ***

User logs out
    Logout
