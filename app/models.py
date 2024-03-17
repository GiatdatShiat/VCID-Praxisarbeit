from flask import url_for
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.VARCHAR(30), unique=True, index=True)
    email = db.Column(db.VARCHAR(30), unique=True, index=True)
    password_hash = db.Column(db.VARCHAR(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    #Password hashen
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    #Check gehashtes Password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    #Aufbereitung der Daten für API-Abfrage
    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            'last_seen': self.last_seen,
            'created_at': self.created_at,
            '_links': {
                'self': url_for('get_user', id=self.id),
            }
        }
        if include_email:
            data['email'] = self.email
        return data
    #Alle Benutzer abfragen
    @staticmethod
    def to_collection():
        users = User.query.all()
        data = {'items': [item.to_dict() for item in users]}
        return data

#User aus der Datenbank lesen, damit Flask-Login den User tracken kann.
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    
class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    photo_ref = db.Column(db.VARCHAR(255))
    filename = db.Column(db.VARCHAR(255))
    filepath = db.Column(db.VARCHAR(255))
    filesize = db.Column(db.Integer)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    average_rating = db.Column(db.Integer)

    def __repr__(self):
        return '<Photo {}>'.format(self.file_path)
    
    #Aufbereitung der Daten für API-Abfrage
    def to_dict(self):
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'filename': self.filename,
            'filepath': self.filepath,
            'upload_date': self.upload_date,
            '_links': {
                'self': url_for('get_photos', id=self.id),
            }
        }
        return data
    #Alle Benutzer abfragen
    @staticmethod
    def to_collection():
        photos = Photo.query.all()
        data = {'items': [item.to_dict() for item in photos]}
        return data

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo_id = db.Column(db.Integer, db.ForeignKey('photo.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    rating = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Rating {}>'.format(self.rating)
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo_id = db.Column(db.Integer, db.ForeignKey('photo.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Comment {}>'.format(self.comment)