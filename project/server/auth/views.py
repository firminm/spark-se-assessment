from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from project.server import bcrypt, db
from project.server.models import User

auth_blueprint = Blueprint('auth', __name__)

class RegisterAPI(MethodView):
    """
    User Registration Resource
    """

    def get(self):
        responseObject = {
            'status': 'success',
            'message': 'Request successful but please send an HTTP POST request to register the user.'
        }
        return make_response(jsonify(responseObject)), 201

    def post(self):
        '''
        cURL command that worked: 
        curl -X POST -H "Content-type: application/json" -d "{\"email\" : \"testuser@testing.com\", \"password\" : \"12345\"}" "http://assessment.519.buspark.io:8000/auth/register"
        '''

        # get the post data
        post_data = request.get_json(); print(request)
        # check if user already exists
        user = User.query.filter_by(email=post_data.get('email')).first()
        if not user:
            try:
                user = User(
                    email=post_data.get('email'),
                    password=post_data.get('password')
                )

                # insert the user
                db.session.add(user)
                db.session.commit()
                # generate the auth token
                auth_token = user.encode_auth_token(user.id)
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return make_response(jsonify(responseObject)), 202


# define the API resources
registration_view = RegisterAPI.as_view('register_api')

# add Rules for API Endpoints
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST', 'GET']
)

class UserIndexAPI(MethodView):
    def get(self):
        users = User.query.all()
        res = []

        for user in users:
            current_user = {
                'id': user.id,
                'email': user.email,
                'admin': user.admin,
                'registered_on': user.registered_on
            }

            res.append(current_user)
        return make_response(jsonify(res)), 201


auth_blueprint.add_url_rule(
    '/users/index',
    
    view_func=UserIndexAPI.as_view('view_api'),
    methods=['GET']
)