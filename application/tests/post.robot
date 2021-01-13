*** Settings ***

Documentation    A test suite for registering.
Resource         resource.robot

*** Test Cases ***

An unauthenticated user cannot access the post submission form
    Given user navigates to the post submission form
    Then page contains the login form

An unauthenticated user cannot create a post by circumventing the post submission form
    Given user tries to create a text post with title "Example" and text "Example content"
    Then page contains the login form
    When user tries to create a link post with title "Example" and url "www.example.com"
    Then page contains the login form

An authenticated user can create a new text post
    Given user "kalle" registers with password "password"
    When user "kalle" logs in with password "password"
    When user tries to create a text post with title "Example post" and text "Example content"
    Then page contains "Example post"

An authenticated user can create a new link post
    Given user "kalle" registers with password "password"
    When user "kalle" logs in with password "password"
    When user tries to create a link post with title "Example link" and url "www.example.com"
    Then page contains "Example link"

*** Keywords ***

User tries to create a text post with title "${title}" and text "${text}"
    Create Post    ${title}    ${EMPTY}     ${text}

User tries to create a link post with title "${title}" and url "${url}"
    Create Post    ${title}    ${url}       ${EMPTY}

User navigates to the post submission form
    Navigate To    /submit