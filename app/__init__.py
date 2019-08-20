from flask import Flask
from flask_login import LoginManager
from config import Config
from app.deep import deep
from app.db import skill, user

app = Flask(__name__)
app.config.from_object(Config)

agent = deep.deep()
login = LoginManager(app)
login.login_view = 'login'
user = user.User()

from app.view import template, api
