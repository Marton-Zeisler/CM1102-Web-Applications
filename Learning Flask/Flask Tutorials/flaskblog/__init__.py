from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "8a149b954839a333daab254096d2561b"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sitme.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category= "info"
app.config["MAIL_SERVER"] = "smptp.googlemail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USERNAME"] = ""
app.config["MAIL_PASSWORD"] = ""
mail = Mail(app)

from flaskblog import routes
from flaskblog.errors.handlers import errors
app.register_blueprint(errors)