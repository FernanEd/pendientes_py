from flask.helpers import flash
from app import app
from flask import render_template, url_for, redirect, request, jsonify
from app.forms import LoginForm, RegisterForm
from flask_login import current_user, login_user, logout_user, login_manager, LoginManager, login_required
from app.models import User
from app import db

# ----[LOGIN]----

login_manager = LoginManager(app)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login?next=' + request.path)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


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
            return redirect(url_for("login"))
        else:
            # TODO: flash "ya estas registrado"-
            return redirect(url_for("index"))
    else:
        return render_template("register.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

# ----[RUTAS]----

@app.route("/")
def index():
    return render_template("index.html")

# ----[API]----

@app.route("/proyectos/", methods=["GET", "POST"])
def proyectos():
    if request.method == 'GET':
        return jsonify('get todos')
    elif request.method == 'POST':
        data = request.get_json(force=True)
        print(data)
        print()
        return jsonify('post todo')
    else:
        return jsonify('a')

@app.route("/proyectos/<int:id>", methods=["GET", "POST"])
def proyecto(id):
    if request.method == 'GET':
        return jsonify('get todos')
    elif request.method == 'POST':
        data = request.get_json(force=True)
        print(data)
        print()
        return jsonify('post todo')
    else:
        return jsonify('a')

