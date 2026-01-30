from app import create_app
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("FLASK_APP_PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
