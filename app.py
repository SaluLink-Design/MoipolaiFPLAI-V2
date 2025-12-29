import os
import logging

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app at module level (required for gunicorn)
from app import create_app

logger.info("Starting FPL AI Backend...")
app = create_app()
logger.info("Flask app created successfully")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Starting development server on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
