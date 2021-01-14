*** Settings ***

Documentation    A test suite for posts.
Library          String
Resource         resource.robot

*** Test Cases ***

An unauthenticated user cannot access the post submission form
    Given user navigates to the post submission form
    Then page contains the login form

An unauthenticated user cannot create a post by circumventing the post submission form
    Given user tries to create a text post with title "Example" and text "Example content"
    Then page contains the login form
    When user tries to create a link post with title "Example", url "http://www.example.com" and no text content
    Then page contains the login form

An authenticated user can create a new text post with optional text content
    Given user "kalle" is authenticated
    When user tries to create a text post with title "Example post" and text "Example content"
    Then page contains a text post with title "Example post"

An authenticated user can create a new text post with just a title
    Given user "kalle" is authenticated
    When user tries to create a text post with title "Example post" and no text content
    Then page contains a text post with title "Example post"

An authenticated user can create a new link post with optional text content
    Given user "kalle" is authenticated
    When user tries to create a link post with title "Example link", url "http://www.example.com" and text "Example text"
    Then page contains a link post with title "Example link" and url "http://www.example.com"

An authenticated user can create a new link post with just a title and an url
    Given user "kalle" is authenticated
    When user tries to create a link post with title "Example link", url "http://www.example.com" and no text content
    Then page contains a link post with title "Example link" and url "http://www.example.com"

An authenticated user cannot create a link post with a title that is too short
    Given user "kalle" is authenticated
    When user tries to create a link post with title "A", url "http://www.example.com" and no text content
    Then page contains "title must be between 2 and 200 characters long"

An authenticated user cannot create a link post with a title that is too long
    Given user "kalle" is authenticated
    When user tries to create a link post with title that is too long
    Then page contains "title must be between 2 and 200 characters long"

An authenticated user cannot create a text post with a title that is too long
    Given user "kalle" is authenticated
    When user tries to create a text post with title that is too long
    Then page contains "title must be between 2 and 200 characters long"

*** Keywords ***

User navigates to the post submission form
    Navigate To    /submit

User tries to create a text post with title "${title}" and text "${text}"
    Create Post    ${title}    ${EMPTY}     ${text}

User tries to create a text post with title "${title}" and no text content
    Create Post    ${title}    ${EMPTY}     ${EMPTY}

User tries to create a link post with title "${title}", url "${url}" and text "${text}"
    Create Post    ${title}    ${url}       ${text}

User tries to create a link post with title "${title}", url "${url}" and no text content
    Create Post    ${title}    ${url}       ${EMPTY}

User tries to create a link post with title that is too long
    ${TOO_LONG_TITLE} =     Generate Random String    201    [LETTERS][NUMBERS]
    Create Post    ${TOO_LONG_TITLE}    ${EXAMPLE_URL}    ${EMPTY}

User tries to create a text post with title that is too long
    ${TOO_LONG_TITLE} =     Generate Random String    201    [LETTERS][NUMBERS]
    Create Post    ${TOO_LONG_TITLE}    ${EMPTY}    ${EMPTY}

Page contains a text post with title "${title}"
    Page Contains    /comments">${title}</a>

Page contains a link post with title "${title}" and url "${url}"
    Page Contains    <a class="content" href=${url}>${title}</a>