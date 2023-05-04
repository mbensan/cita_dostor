from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config.from_pyfile('../config.py')
app.secret_key = app.config['SECRET_KEY']

bcrypt = Bcrypt(app)
