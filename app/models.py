from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(255))
    lastName = db.Column(db.String(255))
    username = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    status = db.Column(db.String(255))
    companyName = db.Column(db.String(255))
    address = db.Column(db.String(255))
    role = db.Column(db.String(255))  # ENUM('super-admin', 'admin', 'user') mapped as String
    mainBranchId = db.Column(db.Integer)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'))
    branchId = db.Column(db.Integer)
    totalAmount = db.Column(db.Numeric(10, 2))
    
    # Required fields from Node.js model
    customerName = db.Column(db.String(255), nullable=False)
    
    # Corrected Status fields
    orderStatus = db.Column(db.String(255), default="WAITING") # Map status -> orderStatus
    orderType = db.Column(db.String(255), default="BULK")
    
    # Other fields
    tableStatus = db.Column(db.String(255), default="AVAILABLE")
    
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    orderId = db.Column(db.Integer, db.ForeignKey('orders.id'))
    
    # Corrected column names based on orderItem.model.js
    itemname = db.Column(db.String(255))
    quantity = db.Column(db.Integer)
    priceperunit = db.Column(db.Numeric(10, 2))
    
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
