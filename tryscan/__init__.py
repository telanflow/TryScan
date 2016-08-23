import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object('config')
app.secret_key = b'P\xcc\x83S/\x91\xf3f\x9a\\G\x1b\xe9\xce\xcd\x9a\xe1lR\x18\xe1\xf6\xc1,'
# os.urandom(24)

login_manage = LoginManager()
login_manage.init_app(app)
login_manage.login_view = 'login'

db = SQLAlchemy(app)

from tryscan import models, views, api





