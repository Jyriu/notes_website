from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('views', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Connexion réussie!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Mot de passe incorrect, réessayez.", category='error')
        else:
            flash("L'adresse email n'existe pas.", category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash("L'adresse email existe déjà.", category='error')
        elif email is None or len(email) < 4:
            flash("L'adresse email doit contenir au moins 4 caractères.", category='error')
        elif firstname is None or len(firstname) < 2:
            flash("Le prénom doit contenir au moins 2 caractères.", category='error')
        elif password1  is None or password2 is None or password1 != password2:
            flash("Les mots de passe ne correspondent pas.", category='error')
        elif password1 is None or len(password1) < 7:
            flash("Le mot de passe doit contenir au moins 7 caractères", category='error')
        else:
            new_user = User(email=email, firstname=firstname, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash("Inscription réussie!", category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)