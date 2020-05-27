from flask import Flask
from flask_cors import CORS, cross_origin

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

from app import routes

CORS(app, support_credentials=True)

if __name__ == '__main__':
    app.run()