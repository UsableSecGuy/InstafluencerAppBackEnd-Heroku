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

If you have virtualenv installed, run:
```bash
python3 -m venv env
source env/bin/activate
```

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
    - {username, full_name, profile_link, profile_pic_link, followers, posts_per_week, engagement, hashtags}
- The SavedInsta table stores the end user's list of saved influencers.
    - { searcher_username, insta_fluencer_id, date_saved}

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

1. ##### POST /insta-fluencers/search
    it searches instafluencer table by hashtag
    it should not require any permission to use
returns status code 200 and json
```
{
    'success': True,
    'insta_fluencers': [<instafluencer 1>,<instafluencer 2>,
    <instafluencer 3>, <instafluencer 4>],
    'total_insta_fluencers': 4,
    'search_term': "college radio"
}
```

2. ##### PATCH /insta-fluencers/\<insta_id>
    where <insta_id> is the existing insta_fluencer_id
    it should respond with a 404 error if <insta_id> is not found
    it should update the corresponding row for <insta_id>
    it should require the 'update:influencer' permission
returns status code 200 and json
```
{"success": True, "insta_fluencer_id": 1}
```

3. ##### GET /saved-insta-fluencers
    it should respond with a 404 error if <insta_id> is not found
    it should update the corresponding row for <insta_id>
    it should require the 'update:influencer' permission
returns status code 200 and json
```
{"success": True,
"saved_list": [<SavedInsta 1>, <SavedInsta 2>],
"total_saved": 2
}
```

4. ##### POST /insta-fluencers
    it should create a new row in the instafluencer table
    it should require the 'add:influencer' permission
returns status code 200 and json
```
{"success": True, "id": instafluencer.id}
```
where instafluencer.id is the id of the newly added instafluencer
    or appropriate status code indicating reason for failure

5. ##### POST /saved-insta-fluencers
    it should create a new row in the savedInsta table
    it should require the 'save:influencer' permission
returns status code 200 and json
```
{"success": True, "id": saved_insta.id}
```
where saved.id is the id of the newly added savedInsta entry
    or appropriate status code indicating reason for failure

6. ##### DELETE /saved-insta-fluencers/\<saved_id>
    where <saved_id> is the existing saved model id
    it should respond with a 404 error if <saved_id> is not found
    it should delete the corresponding row for <saved_id>
    it should require the 'unsave:influencer' permission
returns status code 200 and json
```
{"success": True, "delete": saved_id}
```
where saved_id is the id of the deleted record
    or appropriate status code indicating reason for failure

7. ##### DELETE /insta-fluencers/\<insta_id>
    where <insta_id> is the existing instafluencer model id
    it should respond with a 404 error if <insta_id> is not found
    it should delete the corresponding row for <insta_id>
    it should require the 'delete:influencer' permission
returns status code 200 and json
```
{"success": True,"deleted_id": insta_id}
```
where insta_id is the id of the deleted record
    or appropriate status code indicating reason for failure

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

7. Test endpoints using curl or with [Postman](https://getpostman.com).
    - Register 2 users - assign the Standard role to one and Premium role to the other.
    - Sign into each account and make sure to capture the JWT.
    - ### [Postman tests need to updated; Please use cURL]
    Do not use right now] Import the postman collection `udacity-fsnd-capstone-instafluencer.postman_collection.json`
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
