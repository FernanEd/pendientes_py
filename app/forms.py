from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email

# Forms para las paginas
# Login
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recuerdame')
    submit = SubmitField('Entrar')

# Registro
class RegisterForm (FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    password_confirm = PasswordField('Confirmar contraseña', validators=[DataRequired()])
    submit = SubmitField('Registrarse')

# Proyecto para añadir proyectos o pendientes
class ProyectoForm (FlaskForm):
    name = StringField('Nombre del proyecto o pendiente', validators=[DataRequired()])
    submit = SubmitField('Registrar proyecto o pendiente')