from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

from app import db, login, app


class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    firstname = db.Column(db.String(64), nullable=False)
    lastname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    balance = db.Column(db.Float)
    phone = db.Column(db.Integer, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(24), nullable=False)
    # posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        data = {
            'user_id': self.user_id,
            'username': self.username,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'balance': self.balance,
            'phone': self.phone,
            'password_hash': self.password_hash
        }

        return data

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user


class Genre(db.Model):
    genre_id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    genre = db.Column(db.String(64), unique=True, nullable=False)
    type = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        data = {
            'genre_id': self.genre_id,
            'genre': self.genre,
            'type': self.type
        }

        response = '<Genre %s>' %data
        return repr(response)


class Book(db.Model):
    book_id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    bookname = db.Column(db.String(64), nullable=False)
    image = db.Column(db.BLOB, nullable=False)
    description = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        data = {
            'book_id': self.book_id,
            'book_name': self.bookname,
            'image': self.image,
            'description': self.description
        }

        response = '<Book %s>' %data
        return repr(response)


class Library(db.Model):
    lib_id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    gen_id = db.Column(db.Integer, db.ForeignKey('genre.genre_id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), nullable=False)
    book_name = db.Column(db.Integer, db.ForeignKey('book.bookname'), nullable=False)

    def __repr__(self):
        data = {
            'lib_id': self.lib_id,
            'genre_id': self.gen_id,
            'book_id': self.bo_id,
            'book_name': self.bo_name
        }

        response = '<Library %s>' %data
        return repr(response)


class RateComment(db.Model):
    rate_comment_id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'))
    rate = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)

    def __repr__(self):
        data = {
            'rate_comment_id': self.rate_comment_id,
            'book_id': self.book_id,
            'rate': self.rate,
            'comment': self.comment
        }

        response = '<Rate and Comment %s>' % data
        return repr(response)