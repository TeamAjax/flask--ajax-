from flask import render_template, url_for, flash, redirect, request, jsonify, g
from flask_login import current_user, login_user, logout_user, login_required
import json
from werkzeug.security import generate_password_hash
from app import app, db
from app.models import *
from forms import LoginForm, BookForm
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


@app.route('/')
@app.route('/index')
@auth.login_required
def index():
    return render_template('index.html', title='Home Page')


@app.route('/')
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


# @app.route('/login', methods=['GET','POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user is None or not user.check_password(form.password.data):
#             flash('Invalid username or password')
#             return redirect(url_for('login'))
#         login_user(user, remember=form.remember_me.data)
#         next_page = request.args.get('next')
#         if not next_page or url_parse(next_page).netloc != '':
#             next_page = url_for('index')
#         return redirect(next_page)
#     return render_template('login.html', title='Sign In', form=form)


@app.route('/users/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['POST'])
def register():
    # validate here
    username = request.form['username']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    phone = request.form['phone']
    password = generate_password_hash(request.form['password'])
    password_confirm = generate_password_hash(request.form['password_confirm'])



    user = User(username=username, firstname=firstname, lastname=lastname, email=email, phone=phone, balance=0, role='reader', password_hash=password)
    #db.session.add(user)
    #db.session.commit()
    return jsonify(user.user_obj())


@app.route('/users/', methods=['GET'])
def user_search():
    pass


@app.route('/book', methods=['GET'])
def getAllBook():
    book_list = Book.query.all()
    items = []
    for book in book_list:
        items.append({'book_name': book.bookname, 'img': book.image, 'desc' : book.description })
    return jsonify(items)


@app.route('/addBook', methods=['GET'])
def addBookForm():
    form = BookForm()
    return render_template('addForm.html', form=form)

@app.route('/book', methods=['POST'])
def addBook():
    form = BookForm(request.form)
    bookname = form.bookname.data
    image = form.image.data
    description = form.description.data

    book = Book(bookname=bookname, image=image, description=description)
    db.session.add(book)
    db.session.commit()
    return jsonify([{'book_name':bookname, 'image':image, 'description':description}])

@app.route('/genre', methods=['GET'])
def getAllGenre():
    genre_list = Genre.query.all()
    items = []
    for genre in genre_list:
        items.append({'genre': genre.genre, 'type': genre.type})
    return jsonify(items)

@app.route('/genre1/<category>', methods=['GET', 'POST'])
def searchBookCategory(category):
    book_id = request.form.get('id')
    books = Book.query.get(book_id)
    genre = Genre.query.get(category)
    books.genre.append(genre)

    db.session.add(books)
    db.session.commit()
