from flask import Flask
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def create_app() -> Flask:
    app = Flask(__name__)
    
    # Add CORS support for frontend
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    # Register blueprints
    try:
        from .routes.api import api_bp
        from .routes.views import views_bp
        app.register_blueprint(api_bp, url_prefix="/api")
        app.register_blueprint(views_bp)
        app.logger.info("Blueprints registered successfully")
    except Exception as e:
        app.logger.error(f"Error registering blueprints: {e}")
        raise

    return app
