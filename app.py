import os
import base64
import json
from flask import Flask, request, jsonify, abort
from flask_cors import CORS

from models import db_drop_and_create_all, setup_db, Instafluencer, SavedInsta
from auth.auth import AuthError, requires_auth


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    '''
        Uncomment the following line to initialize the datbase
        !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
        !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
    '''
    # db_drop_and_create_all()
    # minor change added here to test new github heroku connection

    # ROUTES

    '''
        1. POST /insta-fluencers/search
            it searches instafluencer table by hashtag
            it should not require any permission to use
        returns status code 200 and json
        {
            'success': True,
            'insta_fluencers': [<instafluencer 1>,<instafluencer 2>,
            <instafluencer 3>, <instafluencer 4>],
            'total_insta_fluencers': 4,
            'search_term': "college radio"
        }
    '''

    @app.route('/insta-fluencers/search', methods=['POST'])
    def search_insta_fluencers():

        # get request from the client
        body = request.get_json()

        # get info from the body and if nothing there set it to None
        if "search_term" in body:
            search_term = body.get('search_term', None)
        else:
            abort(400)

        # pass to helper function
        if search_term:
            search_results = search_social(search_term)

        else:
            abort(400)

        return search_results.data

    '''
        Helper function that takes in a search term and returns a list
        of influencers, total number in the list, the search_term, and success
        code
    '''
    def search_social(search_term):

        try:

            ''' query Insta db for search_term and arrange by highest engagement
            # goal query in sql to conver to sqlalchemy:
            # select * from instafluencer where 'college radio'=ANY(hashtags)
            # order by engagement desc; '''
            selection = Instafluencer.query.filter(Instafluencer.hashtags.
                                                   any('{}'.format(search_term)
                                                       )
                                                   ).order_by(Instafluencer.
                                                              engagement.desc()
                                                              ).all()

            '''
                {} are placeholders for python format() in strings.
                Using {} as placeholders lets you insert all arguments in the
                following () w/o having to worry about indexes numbering or
                naming it auto fills each placeholder in the order the args
                appear
            '''

            if(len(selection) != 0):

                formatted_selection = []

                for select in selection:

                    formatted_selection.append(
                        {
                            "id": select.id,
                            "username": select.username,
                            "full_name": select.full_name,
                            "profile_pic_link": select.profile_pic_link,
                            "profile_link": select.profile_link,
                            "followers": select.followers,
                            "posts_per_week": select.posts_per_week,
                            "engagement": select.engagement,
                            "hashtags": select.hashtags

                        }
                    )

                return jsonify({
                    'success': True,
                    'search_term': search_term,
                    'total_insta_fluencers': len(formatted_selection),
                    'insta_fluencers': formatted_selection
                })

            else:

                abort(404)

        except BaseException:
            abort(404)

    '''
        2. PATCH /insta-fluencers/<insta_id>
            where <insta_id> is the existing insta_fluencer_id
            it should respond with a 404 error if <insta_id> is not found
            it should update the corresponding row for <insta_id>
            it should require the 'update:influencer' permission
        returns status code 200 and json
        {"success": True, "insta_fluencer_id": 1}
    '''

    @app.route('/insta-fluencers/<int:insta_id>', methods=['PATCH'])
    @requires_auth('update:influencer')
    def update_influencer(jwt, insta_id):
        try:
            instafluencer = Instafluencer.query. \
                filter(Instafluencer.id == insta_id).one_or_none()

            # check if drink even exists
            if instafluencer is None:
                abort(404)

            # get payload for update
            body = request.get_json()

            # see what's being updated and change value
            if "username" in body:
                # get info from the body and if nothing there set it to None
                new_username = body.get('username', None)
                instafluencer.username = new_username

            if "full_name" in body:
                new_full_name = body.get('full_name', None)
                instafluencer.full_name = new_full_name

            if "profile_pic_link" in body:
                new_profile_pic_link = body.get('profile_pic_link', None)
                instafluencer.profile_pic_link = new_profile_pic_link

            if "profile_link" in body:
                new_profile_link = body.get('profile_link', None)
                instafluencer.profile_link = new_profile_link

            if "followers" in body:
                new_followers = body.get('followers', None)
                instafluencer.followers = new_followers

            if "posts_per_week" in body:
                new_posts_per_week = body.get('posts_per_week', None)
                instafluencer.posts_per_week = new_posts_per_week

            if "engagement" in body:
                new_engagement = body.get('engagement', None)
                instafluencer.engagement = new_engagement

            if "hashtags" in body:
                new_hashtags = body.get('hashtags', None)

                # append new hashtag to list
                instafluencer.hashtags.append(new_hashtags)

            instafluencer.update()

            return jsonify({
                "success": True,
                "insta_fluencer_id": instafluencer.id
            })
            '''
            cannot return query result alone; it has to be an attr or custom
            formatted json response. Otherwise code will throw an error.
            '''

        except BaseException:
            abort(404)

    '''
        3. GET /saved-insta-fluencers
            it should respond with a 404 error if <insta_id> is not found
            it should update the corresponding row for <insta_id>
            it should require the 'update:influencer' permission
        returns status code 200 and json
        {"success": True,
        "saved_list": [<SavedInsta 1>, <SavedInsta 2>],
        "total_saved": 2
        }
    '''

    @app.route('/saved-insta-fluencers')
    @requires_auth('view:saved')
    def get_saved(jwt):
        try:
            # use jwt['sub'] because the jwt that is passed is already decoded
            saved_list = SavedInsta.query. \
                filter(SavedInsta.searcher_username == jwt['sub']). \
                order_by('id').all()

            formatted_saved = []

            for save in saved_list:
                formatted_saved.append(
                    {
                        "id": save.id,
                        "insta_fluencer_id": save.insta_fluencer_id,
                        "searcher_username": save.searcher_username
                    }
                )

            return jsonify({
                'success': True,
                'saved_list': formatted_saved,
                'total_saved': len(formatted_saved)
            })

        except BaseException:
            abort(404)

    '''
        4. POST /insta-fluencers
            it should create a new row in the instafluencer table
            it should require the 'add:influencer' permission
        returns status code 200 and json
        {"success": True, "id": instafluencer.id}
        where instafluencer.id is the id of the newly added instafluencer
            or appropriate status code indicating reason for failure
    '''

    @app.route('/insta-fluencers', methods=['POST'])
    @requires_auth('add:influencer')
    def post_instafluencer(jwt):  # add back jwt
        # get request from the client
        body = request.get_json()

        # get info from the body and if nothing there set it to None
        new_username = body.get('username', None)
        new_full_name = body.get('full_name', None)
        new_profile_pic_link = body.get('profile_pic_link', None)
        new_profile_link = body.get('profile_link', None)
        new_followers = body.get('followers', None)
        new_posts_per_week = body.get('posts_per_week', None)
        new_engagement = body.get('engagement', None)
        new_hashtags = body.get('hashtags', None)

        try:

            instafluencer = Instafluencer(
                username=new_username,
                full_name=new_full_name,
                profile_pic_link=new_profile_pic_link,
                profile_link=new_profile_link,
                followers=new_followers,
                posts_per_week=new_posts_per_week,
                engagement=new_engagement,
                hashtags=new_hashtags)

            instafluencer.insert()

            return jsonify({
                "success": True,
                "id": instafluencer.id
            })

        except BaseException:
            abort(400)

    '''
        5. POST /saved-insta-fluencers
            it should create a new row in the savedInsta table
            it should require the 'save:influencer' permission
        returns status code 200 and json
        {"success": True, "id": saved_insta.id}
        where saved.id is the id of the newly added savedInsta entry
            or appropriate status code indicating reason for failure
    '''

    @app.route('/saved-insta-fluencers', methods=['POST'])
    @requires_auth('save:influencer')
    def post_saved(jwt):
        # get request from the client
        body = request.get_json()

        # get info from the body and if nothing there set it to None
        new_username = body.get('searcher_username', None)
        new_insta_fluencer_id = body.get('insta_fluencer_id', None)

        try:

            saved_insta = SavedInsta(
                searcher_username=new_username,
                insta_fluencer_id=new_insta_fluencer_id)

            results = SavedInsta.query.filter(SavedInsta.searcher_username ==
                                              saved_insta.searcher_username,
                                              SavedInsta.insta_fluencer_id ==
                                              saved_insta.insta_fluencer_id
                                              ).first()

            if results:
                abort(400)
            else:
                saved_insta.insert()

                return jsonify({
                    "success": True,
                    "id": saved_insta.id
                })

        except BaseException:
            abort(400)

    '''
        6. DELETE /saved-insta-fluencers/<saved_id>
            where <saved_id> is the existing saved model id
            it should respond with a 404 error if <saved_id> is not found
            it should delete the corresponding row for <saved_id>
            it should require the 'unsave:influencer' permission
        returns status code 200 and json
        {"success": True, "deleted_id": saved_id}
        where saved_id is the id of the deleted record
            or appropriate status code indicating reason for failure
    '''

    @app.route('/saved-insta-fluencers/<int:saved_id>', methods=['DELETE'])
    @requires_auth('unsave:influencer')
    def delete_saved(jwt, saved_id):
        try:

            savedInsta = SavedInsta.query. \
                filter(SavedInsta.insta_fluencer_id == saved_id,
                       SavedInsta.searcher_username == jwt['sub']
                       ).one_or_none()

            if savedInsta is None:
                abort(404)

            # delete question from db
            savedInsta.delete()

            return jsonify({
                "success": True,
                "deleted_id": saved_id
            })

        except BaseException:

            abort(404)

    '''
        7. DELETE /insta-fluencers/<insta_id>
            where <insta_id> is the existing instafluencer model id
            it should respond with a 404 error if <insta_id> is not found
            it should delete the corresponding row for <insta_id>
            it should require the 'delete:influencer' permission
        returns status code 200 and json
        {"success": True,"deleted_id": insta_id}
        where insta_id is the id of the deleted record
            or appropriate status code indicating reason for failure
    '''

    @app.route('/insta-fluencers/<int:insta_id>', methods=['DELETE'])
    @requires_auth('delete:influencer')
    def delete_instafluencer(jwt, insta_id):
        try:
            instafluencer = Instafluencer.query.filter(Instafluencer.id
                                                       == insta_id
                                                       ).one_or_none()

            if instafluencer is None:
                abort(404)

            # delete question from db
            instafluencer.delete()

            return jsonify({
                "success": True,
                "deleted_id": insta_id
            })

        except BaseException:

            abort(404)

    # Error Handling
    '''
        Error handler for 422
    '''
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                        "success": False,
                        "error": 422,
                        "message": "unprocessable"
                        }), 422

    '''
        Error handler for 404
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
                        "success": False,
                        "error": 404,
                        "message": "resource not found"
                        }), 404

    '''
        Error handler for 400
    '''
    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": 'bad request'
        }), 400

    '''
        Error handler for 401
    '''
    @app.errorhandler(401)
    def no_authorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": 'not authorized'
        }), 401

    '''
        Error handler for 500
    '''
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": 'Internal Server Error'
        }), 500

    '''
        Error handler for AuthError
        error handler should conform to general task above
    '''

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
