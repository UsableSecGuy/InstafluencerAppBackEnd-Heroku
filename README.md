# Instafluencer Backend

## About

The goal of the Instafluencer App is to allow marketers to search for Instagram nano-influencers with high engagement raters. Marketers can use the Instafluencer App to search Instagram bios for hashtags related to their campaign.

The Instafluencer application endpoints:

1. Searches its own database for Instafluencers  
2. Save lists of Instafluencers.
3. Present Instafluencers in order of highest engagement.

## About the Stack

There is a full backend but a frontend was not required for this assignment (frontend may be added later). It is designed with some key functional areas.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the postgres database.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## DATA MODELING:
#### models.py
The schema for the database and helper methods to simplify API behavior are in models.py:
- There are two tables created: Instafluencer, SavedInsta
- The Instafluencer table is used store specific information of instagram influencers.
- The SavedInsta table stores the end user's list of saved influencers.




## Running The Server (Locally)

From within the directory first ensure you are working using your created virtual environment and install dependencies.

```bash
 python3 -m venv env
 source env/bin/activate
 pip install -r requirements.txt
```


Each time you open a new terminal session, run:

```bash
export FLASK_APP=app.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Running The Server (on Heroku)

The application is live on Heroku. Point your custom cURL or Postman requests [https://instafluencer.herokuapp.com/](https://instafluencer.herokuapp.com/).


## API Endpoints

### View Sample Requests and Responses

[API Documentation via Postman](https://documenter.getpostman.com/view/13069901/TVmJizAo)

### Setup Database For Local Testing
To run the tests, run
```
dropdb instafluencer_app_test
createdb instafluencer_app_test
psql instafluencer_app_test < instafluencer_app_test.psql
```

### Setup Auth0 For Local Testing

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `update:influencer`
    - `save:influencer`
    - `unsave:influencer`
    - `view:saved`
    - `add:influencer`
    - `delete:influencer`
6. Create new roles (Standard, Premium):
    - Standard
        - can `update:influencer`
        - can `save:influencer`
        - can `unsave:influencer`
        - can `view:saved`
    - Premium
        - can perform all restricted actions of the Standard role
        - can `add:influencer`
        - can `delete:influencer`
    - Public (functions anyone can do; do not need a role/permission defined)
        - can `search:influencers`
        - can `view:influencers`

7. Test your endpoints with [Postman](https://getpostman.com).
    - Register 2 users - assign the Standard role to one and Premium role to the other.
    - Sign into each account and make sure to capture the JWT.
    - Import the postman collection `udacity-fsnd-capstone-instafluencer.postman_collection.json`
    - Right-clicking the collection folder for Standard and Premium, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
    - Run the collection.

###### Note 1: For the Udacity Fullstack Nanodegree purposes, the jwt tokens will be included in the postman collection until the submission has been graded.

###### Note 2: For the Udacity Fullstack Nanodegree purposes, PREMUSER and STANDUSER are export variables included in the setup bash file with corresponding jwt tokens for testing using the unittest library. Modifications will be following the assignment being graded.

### Setup For Local Testing Using Unittest
To run the tests, run
```bash
source setup.sh
python test_app.py
```
