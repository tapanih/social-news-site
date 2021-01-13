*** Settings ***

Documentation    A test suite for registering.
Resource         resource.robot

*** Test Cases ***

User cannot register when passwords do not match
    Given user registers with username "matti", password "secret" and password confirmation "wrong"
    Then page contains "passwords do not match"

User cannot register with an username shorter than 3 characters
    Given user registers with username "aa", password "secret" and password confirmation "secret"
    Then page contains "username must be between 3 and 40 characters long"

User cannot register with an username longer than 40 characters
    Given user registers with username "this_username_is_fortyone_characters_long", password "secret" and password confirmation "secret"
    Then page contains "username must be between 3 and 40 characters long"

User cannot register with an username that is already taken
    Given user "matti" registers with password "secret"
    Given user registers with username "matti", password "hunter2" and password confirmation "hunter2"
    Then page contains "username taken"

User can register with a valid username and matching passwords
    Given user registers with username "pekka", password "hunter2" and password confirmation "hunter2"
    Then page contains the login form

*** Keywords ***
User registers with username "${username}", password "${password}" and password confirmation "${confirm_password}"
    Register     ${username}    ${password}    ${confirm_password}

Page contains the login form
    Page Contains    ${LOGIN_FORM}