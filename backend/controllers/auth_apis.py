from flask_restful import Resource
from flask import request, jsonify,make_response
from flask_security import utils,auth_token_required,roles_required
from controllers.user_datastore import user_datastore,db

class LoginAPI(Resource):
    def post(self):
        login_credentials = request.get_json()
        if not login_credentials :
            result={
                'message':'Login credentials are required'
            }
            return make_response(jsonify(result),400)
        email = login_credentials.get('email')
        password = login_credentials.get('password')

        if not email or not password:
            result={
                'message':'Email and password are required'
            }
            return make_response(jsonify(result),400)
        
        user=user_datastore.find_user(email=email)
        if not user:
            result={
                'message':'User not found'
            }
            return make_response(jsonify(result),404)
        

        if not utils.verify_password(password, user.password):
            result={
                'message':'Invalid password'
            }
            return make_response(jsonify(result),401)
        
        auth_token = user.get_auth_token()

        utils.login_user(user)
        result={
            'message':'Login successful',
            'user':{
                'email':user.email,
                'roles':[role.name for role in user.roles],
                'auth_token': auth_token
            } 
        }
        return make_response(jsonify(result),200)
    
class LogoutAPI(Resource):
    @auth_token_required
    def post(self):
        
        utils.logout_user()
        result={
            'message':'Logout successful'
        }
        return make_response(jsonify(result),200)    
    
class RegisterAPI(Resource):
    def post(self):
        
        creds=request.get_json()
        if not creds:
            result={
                'message':'Registration credentials are required'
            }
            return make_response(jsonify(result),400)
        
        email=creds.get('email')
        password=creds.get('password')

        if not email or not password:
            result={
                'message':'Email and password are required'
            }
            return make_response(jsonify(result),400)   
        
        if user_datastore.find_user(email=email):
            result={
                'message':'User with this email already exists'
            }
            return make_response(jsonify(result),409)
        
        user_role=user_datastore.find_role('user')
        user_datastore.create_user(email=email,password=password,roles=[user_role])
        db.session.commit()
        result={
            'message':'User registered successfully',
            'user':{
                'email':email,
                'roles':[role.name for role in user_datastore.find_user(email=email).roles]
            }
        }
        return make_response(jsonify(result),201)
