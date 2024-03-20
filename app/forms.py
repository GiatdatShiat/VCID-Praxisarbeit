from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import data_required, ValidationError, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app.models import User
from app import photos

#Definition der Klasse und der Variablen für das Anmeldeformular.
class LoginForm(FlaskForm):
    username = StringField('Benutzername', validators=[data_required()])
    password = PasswordField('Passwort', validators=[data_required()])
    remember_me = BooleanField('Eingeloggt bleiben')
    submit = SubmitField('Anmelden')

#Definition der Klasse und der Variablen für das Registrierungsformular.
class RegistrationForm(FlaskForm):
    username = StringField('Benutzername', validators=[data_required()])
    email = StringField('Email', validators=[data_required(), Email()])
    password = PasswordField('Passwort', validators=[data_required()])
    password2 = PasswordField(
        'Passwort wiederholen', validators=[data_required(), EqualTo('password')])
    submit = SubmitField('Registrieren')

    #Überprüfung der Benutzernamen auf Eindeutigkeit.
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Dieser Benutzername ist bereits vergeben. Bitte wähle einen anderen.')
        
    #Überprüfung der Email-Adressen auf Eindeutigkeit.    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Es existiert bereits ein Konto mit dieser Mail-Adresse. Bitte wähle eine andere.')

#Definition der Klasse und der Variablen für das Uploadformular.        
class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, 'Nur Bilder sind erlaubt.'),
            FileRequired('Bitte wähle eine Bilddatei aus, die du hochladen möchtest.')
        ]
    )

    submit = SubmitField('Hochladen')