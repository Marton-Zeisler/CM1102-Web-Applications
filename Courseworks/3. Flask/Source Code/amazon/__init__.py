from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "e1df1e854de06a7af786c362991a8cff9a8f4052bc7d874e"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://c1841485:6Z=q]K~GXKzcjW=d@csmysql.cs.cf.ac.uk:3306/c1841485"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category= "info"

from amazon import routes
