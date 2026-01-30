from flask import Flask
from .config import Config
from .models import db
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    db.init_app(app)
    
    with app.app_context():
        # Import parts of our application
        from . import routes
        
        # Register Blueprints
        app.register_blueprint(routes.bp)
        
        # Create tables only if they don't exist (optional, mostly relying on existing DB)
        # db.create_all()

    return app
