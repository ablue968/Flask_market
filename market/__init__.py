from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = '8331f73f826002236d8834c7'
db=SQLAlchemy(app)
bcrypt  = Bcrypt(app)
login_manager = LoginManager(app)

from market import routes