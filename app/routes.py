# app/routes.py
import os
from flask import render_template, flash, redirect, url_for, request, url_for, send_from_directory
from app import app, db
from app.forms import LoginForm, RegistrationForm, UploadForm
from app.models import User, Photo
from flask_login import login_user, current_user, logout_user, login_required
from urllib.parse import urlsplit
from datetime import datetime
from app import photos


#Route zur Hauptseite
@app.route('/')
@app.route('/index')
@login_required
def index():
   return render_template('index.html', title='Home')

#Route zur Login Seite
@app.route('/login', methods=['GET', 'POST'])
def login():
   if current_user.is_authenticated:
      return redirect(url_for('index'))
   form = LoginForm()
   if form.validate_on_submit():
      # Route /login wurde mit POST betreten. Prüfung, ob alles o.k. ist:
      user = User.query.filter_by(username=form.username.data).first()
      if user is None or not user.check_password(form.password.data):
         flash('Ungültiger Benutzername oder Passwort')
         return redirect(url_for('login'))
      # Alles o.k., Login kann erfolgen
      login_user(user, remember=form.remember_me.data)
      next_page = request.args.get('next')
      if not next_page or urlsplit(next_page).netloc != '':
         next_page = url_for('index')
      return redirect(next_page)
   return render_template('login.html', title='Sign In', form=form)

#Route zur Logout Seite
@app.route('/logout')
def logout():
   logout_user()
   return redirect(url_for('index'))

#Route zur Registrierung
@app.route('/register', methods=['GET', 'POST'])
def register():
   if current_user.is_authenticated:
      return redirect(url_for('index'))
   form = RegistrationForm()
   if form.validate_on_submit():
      # Route /register wurde mit POST betreten. Prüfung, ob alles o.k. ist:
      user = User(username=form.username.data, email=form.email.data)
      user.set_password(form.password.data)
      db.session.add(user)
      db.session.commit()
      flash('Gratuliere, du hast dich erfolgreich registriert!')
      return redirect(url_for('login'))
   # Route /register wurde mit GET betreten
   return render_template('register.html', title='Register', form=form)

#Route zum Benutzerprofil
@app.route('/user/<username>')
@login_required
def user(username):
   user = User.query.filter_by(username=username).first_or_404()
   photo = [
      {'author': user, 'body': 'Test post #1'},
      {'author': user, 'body': 'Test post #1'},
   ]
   #Hier "Posts" wieder ersetzen!!
   return render_template('user.html', user=user, photo=photo)

@app.route('/bilder/<filename>')
def get_file(filename):
   return send_from_directory(app.config["UPLOADED_PHOTOS_DEST"], filename)

#Foto hochladen. Code von hier: https://www.youtube.com/watch?v=dP-2NVUgh50
@app.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():
   form = UploadForm()
   if form.validate_on_submit():
      filename = photos.save(form.photo.data)
      file_url = url_for('get_file', filename=filename)
      photo = Photo(user_id=current_user.id, filename=filename, filepath=file_url)
      db.session.add(photo)
      db.session.commit()
   else:
      file_url = None
   return render_template('upload.html', form=form, file_url=file_url)

@app.route('/gallery')
@login_required
def gallery():
   #image_names = os.listdir('bilder')
   image_names = os.listdir('/home/img')
   print(image_names)
   return render_template("gallery.html", image_names=image_names)

#Last_seen abfüllen
@app.before_request
def before_request():
   if current_user.is_authenticated:
      current_user.last_seen = datetime.utcnow()
      db.session.commit()