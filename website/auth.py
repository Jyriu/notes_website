from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

auth = Blueprint('views', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template("login.html", boolean=True)

@auth.route('/logout')
def logout():
    return "<p>Se déconnecter</p>"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if email is None or len(email) < 4:
            flash("L'adresse email doit contenir au moins 4 caractères.", category='error')
        elif first_name is None or len(first_name) < 2:
            flash("Le prénom doit contenir au moins 2 caractères.", category='error')
        elif password1  is None or password2 is None or password1 != password2:
            flash("Les mots de passe ne correspondent pas.", category='error')
        elif password1 is None or len(password1) < 7:
            flash("Le mot de passe doit contenir au moins 7 caractères", category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("Inscription réussie!", category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html")