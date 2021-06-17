from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
  id                =db.Column(db.Integer, primary_key=True)
  email             =db.Column(db.String(120), index=True, unique=True)
  password_hash     =db.Column(db.String(128)) 
  
  def set_password(self, password):
    self.password_hash =generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

  # Relaciones
  proyectos         =db.relationship("Proyecto", backref="Usuario", lazy="dynamic")

  def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Proyecto(db.Model):
  id                =db.Column(db.Integer, primary_key=True)
  title             =db.Column(db.String(100))
  desc              =db.Column(db.String(255))
  id_user           =db.Column(db.Integer, db.ForeignKey("user.id"))

  # Relaciones
  pendientes        =db.relationship("Pendiente", backref="Proyecto", lazy="dynamic")

  def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Pendiente(db.Model):
  id                =db.Column(db.Integer, primary_key=True)
  title             =db.Column(db.String(100))
  desc              =db.Column(db.String(255))
  prior             =db.Column(db.Integer)
  due_date          =db.Column(db.DateTime)
  completed         =db.Column(db.Boolean, default=False)
  id_proyecto       =db.Column(db.Integer, db.ForeignKey("proyecto.id"))

  def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

@login.user_loader
def load_user(id):
    return User.query.get(int(id))