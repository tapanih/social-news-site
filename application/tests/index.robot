*** Settings ***

Resource    resource.robot

*** Test Cases ***

Main page works correctly
    Given user navigates to the main page
    Then page contains "log in"
    Then page contains "register"

*** Keywords ***
User navigates to the main page
    Navigate To    /
