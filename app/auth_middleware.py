from functools import wraps
from flask import request, jsonify, current_app
import jwt
from .models import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check for x-access-token header (matching Node.js app)
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
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
        except Exception as e:
            return jsonify({'message': 'Token is invalid!', 'error': str(e)}), 401
            
        return f(current_user, *args, **kwargs)
    
    return decorated
