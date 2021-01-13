*** Settings ***

Documentation    A resource file with reusable keywords
Library          FlaskLibrary.py

*** Variables ***

${LOGIN_FORM}     <form method="POST" action="/auth/login">

*** Keywords ***

User "${username}" registers with password "${password}"
    Register     ${username}    ${password}    ${password}

User "${username}" logs in with password "${password}"
    Login   ${username}    ${password}

Page contains "${text}"
    Page Contains    ${text}

Page does not contain "${text}"
    Page Not Contains    ${text}