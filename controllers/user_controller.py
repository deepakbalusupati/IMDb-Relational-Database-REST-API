from flask_restful import Resource, reqparse
from flask import jsonify, request
from models.user_model import UserModel
from werkzeug.security import generate_password_hash

class Users(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('per_page', type=int, default=10)
        args = parser.parse_args()
        
        offset = (args['page'] - 1) * args['per_page']
        cursor = UserModel.mysql.connection.cursor()
        cursor.execute("SELECT user_id, username, email, created_at FROM users LIMIT %s OFFSET %s", 
                      (args['per_page'], offset))
        users = cursor.fetchall()
        cursor.close()
        return jsonify({'users': users, 'page': args['page'], 'per_page': args['per_page']})

    def post(self):
        data = request.get_json()
        
        required_fields = ['username', 'email', 'password']
        if not all(field in data for field in required_fields):
            return {'message': 'Missing required fields'}, 400
        
        # Check if username or email already exists
        if UserModel.get_user_by_username(data['username']):
            return {'message': 'Username already exists'}, 400
        if UserModel.get_user_by_email(data['email']):
            return {'message': 'Email already exists'}, 400
        
        user_id = UserModel.create_user(data['username'], data['email'], data['password'])
        return {'message': 'User created successfully', 'user_id': user_id}, 201

class User(Resource):
    def get(self, user_id):
        user = UserModel.get_user_by_id(user_id)
        if user:
            # Don't return password hash
            return jsonify({
                'user_id': user['user_id'],
                'username': user['username'],
                'email': user['email'],
                'created_at': user['created_at']
            })
        return {'message': 'User not found'}, 404

    def put(self, user_id):
        data = request.get_json()
        
        # Check if user exists
        user = UserModel.get_user_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        
        # Check if new username or email already exists
        if 'username' in data and data['username'] != user['username']:
            if UserModel.get_user_by_username(data['username']):
                return {'message': 'Username already exists'}, 400
        if 'email' in data and data['email'] != user['email']:
            if UserModel.get_user_by_email(data['email']):
                return {'message': 'Email already exists'}, 400
        
        if UserModel.update_user(user_id, data):
            return {'message': 'User updated successfully'}, 200
        return {'message': 'User update failed'}, 400

    def delete(self, user_id):
        if UserModel.delete_user(user_id):
            return {'message': 'User deleted successfully'}, 200
        return {'message': 'User not found'}, 404

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        
        if 'username' not in data or 'password' not in data:
            return {'message': 'Missing username or password'}, 400
        
        user = UserModel.verify_user(data['username'], data['password'])
        if user:
            # In a real app, you would generate a JWT token here
            return {
                'message': 'Login successful',
                'user': {
                    'user_id': user['user_id'],
                    'username': user['username'],
                    'email': user['email']
                }
            }, 200
        return {'message': 'Invalid username or password'}, 401