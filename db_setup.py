from flask_sqlalchemy import SQLAlchemy
from app_setup import app
from flask_login import LoginManager

app.secret_key = 'some secret key'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user_data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = True
db = SQLAlchemy(app)
manager = LoginManager(app)
