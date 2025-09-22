from flask import Blueprint

# Views blueprint for HTML pages
views_bp = Blueprint("views", __name__)


@views_bp.get("/")
def index():
    from flask import render_template
    return render_template("index.html")


# API blueprint for JSON endpoints
api_bp = Blueprint("api", __name__)


@api_bp.get("/health")
def health_check():
    return {"status": "ok"}

