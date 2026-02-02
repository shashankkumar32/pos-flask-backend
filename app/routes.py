from flask import Blueprint, request, jsonify, current_app
from .models import db, Order, OrderItem, User, License
from .auth_middleware import token_required
import bcrypt
import jwt
import datetime
import json

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.datetime.utcnow().isoformat()}), 200

@bp.route('/auth/electron/signin', methods=['POST'])
def electron_signin():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    machine_id = data.get('machineId')
    
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400
        
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
        
    # Verify password
    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return jsonify({'message': 'Invalid password'}), 401
        
    # License & Machine ID Logic
    license_info = License.query.filter_by(userId=user.id).first()
    machine_warning = False
    
    if not license_info:
        # First time login with this machine
        license_info = License(
            userId=user.id,
            machineId=machine_id,
            status='ACTIVE',
            previousMachineIds=json.dumps([machine_id])
        )
        db.session.add(license_info)
    else:
        if license_info.machineId != machine_id:
            machine_warning = True
            # Update history if not already there
            previous_ids = json.loads(license_info.previousMachineIds or '[]')
            if machine_id not in previous_ids:
                previous_ids.append(machine_id)
                license_info.previousMachineIds = json.dumps(previous_ids)
            # Update lastLogin nonetheless
        license_info.lastLogin = datetime.datetime.utcnow()
    
    db.session.commit()
    
    # Generate 15-day token
    token = jwt.encode({
        'id': user.id,
        'role': user.role,
        'mainBranchId': user.mainBranchId,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=15)
    }, current_app.config['SECRET_KEY'], algorithm=current_app.config['JWT_ALGORITHM'])
    
    return jsonify({
        'accessToken': token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'mainBranchId': user.mainBranchId,
            'licenseKey': license_info.licenseKey
        },
        'machineWarning': machine_warning,
        'message': 'Login successful' if not machine_warning else 'Logged in from a non-registered system'
    }), 200

@bp.route('/orders/bulk', methods=['POST'])
@token_required
def bulk_create_orders(current_user):
    data = request.get_json()
    
    if not isinstance(data, list):
         return jsonify({'message': 'Input must be a JSON array of orders'}), 400
         
    created_orders = []
    errors = []
    
    try:
        # Transaction block
        for index, order_data in enumerate(data):
            try:
                # Basic Validation
                if 'totalAmount' not in order_data:
                    raise ValueError("Missing totalAmount")
                
                new_order = Order(
                    userId=current_user.id,
                    branchId=current_user.mainBranchId, # Assign to user's main branch
                    totalAmount=order_data.get('totalAmount'),
                    
                    # New Fields mapping
                    tableNumber=order_data.get('tableNumber'),
                    customerPhone=order_data.get('customerPhone'),
                    customerEmail=order_data.get('customerEmail'),
                    notes=order_data.get('notes'),
                    
                    # Map 'status' to 'orderStatus'
                    orderStatus=order_data.get('status', 'WAITING'),
                    # Required field - default if not provided
                    customerName=order_data.get('customerName', 'Bulk Customer'),
                    # Default type for these imports - default now empty string
                    orderType=order_data.get('orderType', ''),
                    
                    # New Financial Fields
                    invoiceId=order_data.get('invoiceId'),
                    paymentMethod=order_data.get('paymentMethod'),
                    discount=order_data.get('discount', 0),
                    serviceCharge=order_data.get('serviceCharge', 0),
                    gstRate=order_data.get('gstRate', 0),
                    appliedCharges=json.dumps(order_data.get('appliedCharges', [])),
                    date=datetime.datetime.fromisoformat(order_data.get('date').replace('Z', '+00:00')) if order_data.get('date') else datetime.datetime.utcnow()
                )
                db.session.add(new_order)
                db.session.flush() # Flush to get order ID
                
                # Process Order Items
                items = order_data.get('items', [])
                for item in items:
                    new_item = OrderItem(
                        orderId=new_order.id,
                        # Map input 'name' -> DB 'itemname'
                        itemname=item.get('name'),
                        quantity=item.get('quantity'),
                        # Map input 'price' -> DB 'priceperunit'
                        priceperunit=item.get('price')
                    )
                    db.session.add(new_item)
                
                created_orders.append({'index': index, 'orderId': new_order.id})
                
            except Exception as e:
                errors.append({'index': index, 'error': str(e)})
                
        if errors:
            db.session.rollback()
            return jsonify({'message': 'Bulk creation failed due to errors in some items', 'errors': errors}), 400
            
        db.session.commit()
        return jsonify({'message': 'Bulk orders created successfully', 'created_count': len(created_orders)}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Server Error during bulk processing', 'error': str(e)}), 500
