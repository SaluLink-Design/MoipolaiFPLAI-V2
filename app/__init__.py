from flask import Flask

def create_app() -> Flask:
    app = Flask(__name__)

    # Register blueprints
    from .routes.api import api_bp
    from .routes.views import views_bp
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(views_bp)

    return app
