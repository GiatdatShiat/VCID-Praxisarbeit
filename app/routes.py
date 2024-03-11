# app/routes.py
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Photo
from flask_login import login_user, current_user, logout_user, login_required
from urllib.parse import urlsplit


#Route zur Hauptseite
@app.route('/')
@app.route('/index')
@login_required
def index():
   user = {'username': 'Jochen'}
   posts = [
   {
   'author': {'username': 'Paul'},
   'body': 'Schöner Abend hier in Zürich!'
   },
   {
   'author': {'username': 'Susanne'},
   'body': 'Der Unterricht war heute mal gut!'
   }
   ]

   return render_template('index.html', title='Home', posts=posts)

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
         flash('Invalid username or password')
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
      flash('Congratulations, you are now a registered user!')
      return redirect(url_for('login'))
   # Route /register wurde mit GET betreten
   return render_template('register.html', title='Register', form=form)

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

#Route für den Upload von Photos.
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        photo = request.files['photo']
        if photo:
            filename = photo.save('static/uploads')
            # Speichere die Foto-Referenz in der Datenbank
            user_id = current_user.id
            photo_ref = Photo(filename=filename, user_id=user_id)
            db.session.add(photo_ref)
            db.session.commit()
            photo_url = url_for('static', filename='uploads/' + filename)
            return 'Foto hochgeladen! URL: {}'.format(photo_url)
        else:
            return 'Fehler beim Hochladen des Fotos.'
    return render_template('upload.html')
