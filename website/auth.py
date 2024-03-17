from flask import Blueprint, render_template, request, flash

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
        firstname = request.form.get('firstname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash("L'adresse email doit contenir au moins 4 caractères.", category='error')
        elif len(firstname) < 2:
            flash("Le prénom doit contenir au moins 2 caractères.", category='error')
        elif password1 != password2:
            flash("Les mots de passe ne correspondent pas.", category='error')
        elif len(password1) < 7:
            flash("Le mot de passe doit contenir au moins 7 caractères", category='error')
        else:
            flash("Inscription réussie!", category='success')
            # ajouter l'utilisateur à la base de données
    return render_template("sign_up.html")