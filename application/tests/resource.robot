*** Settings ***

Documentation    A resource file with reusable keywords
Library          FlaskLibrary.py

*** Variables ***

${LOGIN_FORM}     <form method="POST" action="/auth/login
${TOO_LONG_TITLE}    this title is too long aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
${EXAMPLE_URL}    http://www.example.com

*** Keywords ***

User "${username}" registers with password "${password}"
    Register     ${username}    ${password}    ${password}

User "${username}" logs in with password "${password}"
    Login   ${username}    ${password}

User "${username}" is authenticated
    Register     ${username}    password    password
    Login   ${username}    password

Page contains "${text}"
    Page Contains    ${text}

Page contains the login form
    Page Contains    ${LOGIN_FORM}

Page does not contain "${text}"
    Page Not Contains    ${text}