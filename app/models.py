from flask import url_for
from datetime import datetime, timezone
from flask_login import UserMixin
from sqlalchemy import func, UniqueConstraint
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login

#Definition der Benutzertabelle und deren Attribute.
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.VARCHAR(30), unique=True, index=True)
    email = db.Column(db.VARCHAR(30), unique=True, index=True)
    password_hash = db.Column(db.VARCHAR(256))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    last_seen = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    #Definition der Variablen für die Beziehung zwischen Benutzer und Fotos/Ratings
    photos = db.relationship('Photo', backref='user', lazy=True)
    ratings = db.relationship('Rating', backref='user', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    #Password hashen
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    #Check des gehashten Passwords
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    #Aufbereitung der Benutzerdaten für API-Abfrage.
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

#Definition der Fototabelle und deren Attribute.
class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    photo_ref = db.Column(db.VARCHAR(255))
    filename = db.Column(db.VARCHAR(255))
    filepath = db.Column(db.VARCHAR(255))
    filesize = db.Column(db.Integer)
    upload_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    average_rating = db.Column(db.Integer)

    #Definition der Variable für die Beziehung zwischen Fotos und deren Ratings
    ratings = db.relationship('Rating', backref='photo', lazy=True)

    #Definition des durchschnittlichen Ratings für die Ausgabe auf der Webpage.
    def average_rating_score(self):
        return db.session.query(func.avg(Rating.rating)).filter(Rating.photo_id == self.id).scalar() or 0

    #Definition des Dateipfades für die Ausgabe auf der Webpage.
    def __repr__(self):
        return '<Photo {}>'.format(self.file_path)
    
    #Aufbereitung der Daten der Fotos für API-Abfrage
    def to_dict(self):
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'filename': self.filename,
            'filepath': self.filepath,
            'upload_date': self.upload_date,
            '_links': {
                'self': url_for('get_photo', id=self.id),
            }
        }
        return data
    
    #Alle Fotodaten abfragen
    @staticmethod
    def to_collection():
        photos = Photo.query.all()
        data = {'items': [item.to_dict() for item in photos]}
        return data

#Definition der Ratingtabelle und deren Attribute.
class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo_id = db.Column(db.Integer, db.ForeignKey('photo.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    rating = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    #Benutzer dürfen Foto nur einmal bewerten!
    __table_args__ = (
        UniqueConstraint('user_id', 'photo_id', name='_user_photo_uc'),
    )

    def __repr__(self):
        return '<Rating {}>'.format(self.rating)

#Definition der Ratingtabelle und deren Attribute.
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo_id = db.Column(db.Integer, db.ForeignKey('photo.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment = db.Column(db.Text)
    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return '<Comment {}>'.format(self.comment)