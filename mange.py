# app launcher

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# app.config.from_pyfile('config.py')

app.config["DEBUG"] = True
app.config["SECRET_KEY"] = 'super-key'

# MySQL setting
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="uripeled23",
    password="2@WUxjwYxCvz9Km",
    hostname="uripeled23.mysql.pythonanywhere-services.com",
    databasename="uripeled23$comments",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

from views import *

if __name__ == '__main__':
    app.run()
