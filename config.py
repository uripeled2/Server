DEBUG = False
SECRET_KEY = 'super-key'

# MySQL setting
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="uripeled23",
    password="2@WUxjwYxCvz9Km",
    hostname="uripeled23.mysql.pythonanywhere-services.com",
    databasename="uripeled23$comments",
)
SQLALCHEMY_POOL_RECYCLE = 299
SQLALCHEMY_TRACK_MODIFICATIONS = False
