from flask import Blueprint, request, jsonify
from .models import db, Order, OrderItem
from .auth_middleware import token_required

bp = Blueprint('api', __name__, url_prefix='/api')

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
                    orderType=order_data.get('orderType', '')
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
