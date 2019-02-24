from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "Y@\x92\xc6\x02\xc4\xd91Yn\x1a\x07'\xef\xbc\x88\xb36\x1e\x0f2\x94\xb4\xc7"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c1841485:ZAZA23appstore@csmysql.cs.cf.ac.uk:3306/c1841485'

db = SQLAlchemy(app)

from shop import routes
