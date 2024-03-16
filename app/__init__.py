import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, IMAGES
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app,db)

#Initialisierung LoginManager
login = LoginManager(app)
login.login_view = 'login'

# Konfiguration für den Foto-Upload
photos = UploadSet("photos", IMAGES)
app.config["UPLOADED_PHOTOS_DEST"] = "bilder"
#app.config["UPLOADED_PHOTOS_DEST"] = "/home/img"
#Secret Key für Bild-Upload
app.config["SECRET_KEY"] = os.urandom(24)
configure_uploads(app, photos)

from app import routes, models