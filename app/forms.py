from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email

# Forms para las paginas
# Login
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message='Por favor llene el campo')])
    password = PasswordField('Contraseña', validators=[DataRequired(message='Por favor llene el campo')])
    remember_me = BooleanField('Recuerdame')
    submit = SubmitField('Entrar')

# Registro
class RegisterForm (FlaskForm):
    email = StringField('Email', validators=[DataRequired(message='Por favor llene el campo'), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(message='Por favor llene el campo')])
    password_confirm = PasswordField('Confirmar contraseña', validators=[DataRequired(message='Por favor llene el campo')])
    submit = SubmitField('Registrarse')