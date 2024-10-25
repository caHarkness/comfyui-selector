import threading
import logging
import aiohttp
import asyncio

from flask import Flask
from flask import redirect

flask_app = Flask(__name__, static_url_path="", static_folder="static", template_folder="templates")
flask_app.config["TEMPLATES_AUTO_RELOAD"] = True
flask_app.debug = True
flask_app.logger.setLevel(logging.DEBUG)

# Optional, allow Cross Origin Resource Sharing:
# pip install flask-cors

from flask_cors import CORS
CORS(flask_app)

@flask_app.route("/")
def main():
    return redirect("/sessions")

# Load the Flask routing:
from lib.views import *
from lib.v1 import *

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=5000)
