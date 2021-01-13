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

*** Keywords ***
User "${username}" registers with password "${password}"
    Register     ${username}    ${password}    ${password}

User "${username}" logs in with password "${password}"
    Login   ${username}    ${password}
