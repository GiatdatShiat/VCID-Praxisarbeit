from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import data_required, ValidationError, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app.models import User
from app import photos

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[data_required()])
    password = PasswordField('Password', validators=[data_required()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[data_required()])
    email = StringField('Email', validators=[data_required(), Email()])
    password = PasswordField('Password', validators=[data_required()])
    password2 = PasswordField(
        'Repeat Password', validators=[data_required(), EqualTo('password')])
    submit = SubmitField('Register')

    #Überprüfung der Benutzernamen und Email-Adressen auf Eindeutigkeit.
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Dieser Benutzername ist bereits vergeben. Bitte wähle einen anderen.')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Es existiert bereits ein Konto mit dieser Mail-Adresse. Bitte wähle eine andere.')
        
class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, 'Nur Bilder sind erlaubt.'),
            FileRequired('Bitte wähle eine Bilddatei aus, die du hochladen möchtest.')
        ]
    )
    submit = SubmitField('Hochladen')