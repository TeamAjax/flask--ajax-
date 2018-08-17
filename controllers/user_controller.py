from flask import render_template, jsonify, redirect, url_for, request, g, flash
from flask_login import logout_user, current_user, login_user
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm
from app.models import User
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


# @app.route('/')
# @app.route('/index')
# @auth.login_required
@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/')
@app.route('/admin')
@app.route('/users/login', methods=['GET', 'POST'])
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.check_password(password):
            return False
    g.user = user
    return True


@app.route('/users')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/users', methods=['POST'])
def register():
    # validate here
    username = request.form['username']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    phone = request.form['phone']
    password = request.form['password']
    # password_confirm = request.form['password_confirm']

    user = User(
        username=username,
        firstname=firstname,
        lastname=lastname,
        email=email,
        phone=phone,
        balance=0,
        role='reader',
        password_hash=password
    )

    password = user.set_password(password)

    db.session.add(user)
    db.session.commit()
    return jsonify(user.user_reg())


@app.route('/users/<username>', methods=['GET'])
def user_search(username):
    print username
    user = User.query.filter_by(username=username).first()
    user_data = {
        "username": user.username,
        "firstName": user.firstname,
        "lastName": user.lastname,
        "email": user.email,
        "balance": user.balance,
        "phone": user.phone
    }
    return jsonify(user_data), 200
