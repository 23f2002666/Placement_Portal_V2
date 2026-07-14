from flask_restful import Resource
from flask import request, jsonify,make_response
from flask_security import utils,auth_token_required,roles_required,hash_password
from controllers.user_datastore import user_datastore,db
from controllers.models import Student, Company

class LoginAPI(Resource):
    def post(self):
        login_credentials = request.get_json()
        if not login_credentials:
            return {"message": "Login credentials are required"}, 400
        
        email = login_credentials.get('email')
        password = login_credentials.get('password')

        if not email or not password:
            return {"message": "Email and password are required"}, 400
        
        user = user_datastore.find_user(email=email)
        
        if not user:
            return {"message": "User not found"}, 404
        
        
        if not utils.verify_password(password, user.password):
            return {"message": "Invalid password"}, 401

        
        if not user.active:
            return {"message": "Your account is pending admin approval or has been deactivated."}, 403
        
        
        auth_token = user.get_auth_token()
        utils.login_user(user)
        
        return {
            "message": "Login successful",
            "user": {
                "email": user.email,
                "roles": [role.name for role in user.roles],
                "auth_token": auth_token
            }
        }, 200
    
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
        creds = request.get_json()
        if not creds:
            return {"message": "Registration credentials are required"}, 400
        
        email = creds.get('email')
        password = creds.get('password')
        role_name = creds.get('role') 
        
        if not email or not password or not role_name:
            return {"message": "Email, password, and role are required"}, 400
        
        if user_datastore.find_user(email=email):
            return {"message": "User with this email already exists"}, 409

        is_active = True if role_name == 'student' else False

        try:
            role = user_datastore.find_role(role_name)
            user = user_datastore.create_user(
                email=email,
                password=hash_password(password), 
                roles=[role],
                active=is_active
            )
            db.session.commit()

            if role_name == 'student':
                new_profile = Student(
                    user_id=user.id, 
                    full_name=creds.get('full_name', 'New Student'),
                    roll_number=creds.get('roll_number')
                )
            elif role_name == 'company':
                new_profile = Company(
                    user_id=user.id, 
                    company_name=creds.get('company_name', 'New Company'),
                    status='Pending' 
                )
            
            db.session.add(new_profile)
            db.session.commit()

            return {
                "message": f"{role_name.capitalize()} registered successfully. " + 
                           ("Please wait for admin approval." if role_name == 'company' else ""),
                "user_id": user.id
            }, 201

        except Exception as e:
            db.session.rollback()
            return {"message": f"Error during registration: {str(e)}"}, 500