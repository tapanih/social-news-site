# social-news-site

## Description

A social news site with a page that lists posts submitted by users. A post consists of a title and content that can be a link to a news article or simply text. A post can also have zero or more comments. The list or posts can be sorted by date (newest first) or number of upvotes.

Features:

* Anyone can
  * sign up and login
  * browse posts that are sorted by upvotes or date
  * read posts and comments
* Registered users can
  * create posts with a title and either a link or a text
  * edit or delete their posts and comments
  * write comments on posts
  * upvote posts

The application is running at: https://social-news-site.herokuapp.com/

Username and password for test account is "test".

## Documentation

[Database diagram](documentation/database_diagram.md)

[User stories](documentation/user_stories.md)

[User manual](documentation/user_manual.md)

## Set Up Instructions

Clone this repository with
```
git clone https://github.com/tapanih/social-news-site
```
Create a Python virtual environment inside the folder (Python 3.7+ required) and activate it with commands
```
$ cd social-news-site
$ python3 -m venv venv
$ source venv/bin/activate
```
Install dependencies with command
```
(venv) $ pip install -r requirements.txt
```
Run the application with command
```
(venv) $ python run.py
```
The application should now be running at http://127.0.0.1:5000/

### Heroku

The repository contains Procfile and runtime.txt for Heroku configuration. An environment variable needs to be set on Heroku with command
```
(venv) $ heroku config:set HEROKU=1
```
Also a database needs to be created with
```
(venv) $ heroku addons:add heroku-postgresql:hobby-dev
```