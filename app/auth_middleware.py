from functools import wraps
from flask import request, jsonify, current_app
import jwt
from .models import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # 1. Check for x-access-token header (matching Node.js app)
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        # 2. Check for Authorization header
        elif 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(" ")[1]
            else:
                token = auth_header # Allow direct token paste
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            # Decode token using shared secret
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=[current_app.config['JWT_ALGORITHM']])
            current_user = User.query.filter_by(id=data['id']).first()
            
            if not current_user:
                return jsonify({'message': 'User not found!'}), 401
                
        except jwt.ExpiredSignatureError:
             return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
             return jsonify({'message': 'Token is invalid!'}), 401
        except Exception as e:
            # If it's a database connection error or similar server issue
            # Return 500 so the user knows it's a server/DB problem, not an auth problem
            return jsonify({
                'message': 'Internal Server Error (Database likely unreachable or limit reached)',
                'error': str(e)
            }), 500
            
        return f(current_user, *args, **kwargs)
    
    return decorated
