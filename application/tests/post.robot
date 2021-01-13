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

An authenticated user can create a new post
    Given user "kalle" registers with password "password"
    When user "kalle" logs in with password "password"
    When user tries to create a text post with title "Example post" and text "Example content"
    Then page contains "Example post"

*** Keywords ***

User tries to create a text post with title "${title}" and text "${text}"
    Create Post    ${title}    ""     ${text}

User navigates to the post submission form
    Navigate To    /submit