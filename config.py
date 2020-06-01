DEBUG = True
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

# token = eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiIwNDQ3ZTc5ZS1mZTAxLTQxM2ItOTc5Zi0zNThkMmNlZWI4MDkiLCJleHAiOjE1OTA5MTY4NjF9.Jir9cjgoBYpgETyXos87kfArsRed6usY4COAUklb9kQ
