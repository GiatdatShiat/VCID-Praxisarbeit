# app/api.py
from app import app
from app.models import User, Photo
from flask import jsonify

#Definition API-Endpunkt einzelner Benutzer.
@app.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):
    data = User.query.get_or_404(id).to_dict()
    return jsonify(data)

#Definition API-Endpunkt aller Benutzer.
@app.route('/api/users', methods=['GET'])
def get_users():
    data = User.to_collection()
    return jsonify(data)

#Definition API-Endpunkt einzelner Fotos.
@app.route('/api/photos/<int:id>', methods=['GET'])
def get_photo(id):
    data = Photo.query.get_or_404(id).to_dict()
    return jsonify(data)

#Definition API-Endpunkt aller Fotos.
@app.route('/api/photos', methods=['GET'])
def get_photos():
    data = Photo.to_collection()
    return jsonify(data)