from flask.helpers import flash
from app import app
from flask import json, render_template, url_for, redirect, request, jsonify
from app.forms import LoginForm, RegisterForm
from flask_login import current_user, login_user, logout_user, login_manager, LoginManager, login_required
from app.models import Pendiente, Proyecto, User
from app import db

# ----[LOGIN]----

login_manager = LoginManager(app)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login?next=' + request.path)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

# ----[RUTAS]----

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form=LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email = email).first()
        if user is None or not user.check_password(form.password.data):
            flash("Correo o contraseña no validos")
            return redirect(url_for("login"))
        else:
            login_user(user, remember=form.remember_me.data)
        return redirect(url_for("index"))
    else:
        return render_template("login.html", form=form)
    

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form=RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email = email).first()
        if user is None and form.password.data==form.password_confirm.data:
            user = User(email=email)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            return redirect(url_for("index"))
        else:
            flash("El usuario ya existe o tu contraseñas no coincide")
            return redirect(url_for("register"))
    else:
        return render_template("register.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))



@app.route("/")
@login_required
def index():
    return render_template("index.html")

# ----[API]----

## Proyectos

@app.route("/proyectos", methods=["GET", "POST"])
def proyectos():
    if request.method == 'GET':
        proyectos = Proyecto.query.filter_by(id_user=current_user.id).all()
        return jsonify([i.as_dict() for i in proyectos])
    elif request.method == 'POST':
        data = request.get_json(force=True)
        nuevoProyecto = Proyecto(title=data["title"], desc=data["desc"], id_user=current_user.id)
        db.session.add(nuevoProyecto)
        db.session.commit()
        return jsonify(nuevoProyecto.as_dict())
    else:
        return jsonify('error: MAL REQUEST')

@app.route("/proyectos/<int:id>", methods=["GET", "PUT", "DELETE"])
def proyecto(id):
    if request.method == 'GET':
        return jsonify('get todos')
    elif request.method == 'PUT':
        data = request.get_json(force=True)
        proyecto = Proyecto.query.get(id)
        proyecto.title = data["title"]
        proyecto.desc = data["desc"]
        db.session.commit()
        return jsonify(proyecto.as_dict())
        
    elif request.method == 'DELETE':
        print(id)
        borrarProyecto = Proyecto.query.get(id)
        db.session.delete(borrarProyecto)
        db.session.commit()
        return jsonify(borrarProyecto.as_dict())
    else:
        return jsonify('error: MAL REQUEST')

## Pendientes

@app.route("/proyectos/<int:proyectoid>/pendientes/", methods=["GET", "POST"])
def pendientes(proyectoid):
    if request.method == 'GET':
        pendientes = Pendiente.query.filter_by(id_proyecto=proyectoid).all()
        return jsonify([i.as_dict() for i in pendientes])
    elif request.method == 'POST':
        data = request.get_json(force=True)
        nuevoPendiente = Pendiente(desc=data["desc"], priority=data["priority"], id_proyecto=proyectoid)
        db.session.add(nuevoPendiente)
        db.session.commit()
        return jsonify(nuevoPendiente.as_dict())
    else:
        return jsonify('error: MAL REQUEST')

@app.route("/proyectos/<int:proyectoid>/pendientes/<int:pendienteid>", methods=["GET", "PATCH", "DELETE"])
def pendiente(proyectoid, pendienteid):
    if request.method == 'PATCH':
        pendiente = Pendiente.query.get(pendienteid)
        pendiente.completed = False if pendiente.completed else True
        db.session.commit()
        return jsonify(pendiente.as_dict())
    else:
        return jsonify('error: MAL REQUEST')