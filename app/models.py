from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

from app import db, login, app


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    firstname = db.Column(db.String(64), nullable=False)
    lastname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    balance = db.Column(db.Float)
    phone = db.Column(db.Integer, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(24), nullable=False)
    # posts = db.relationship('Post', backref='author', lazy='dynamic')

    def user_obj(self):
        user_data = {
            'id': self.id,
            'username': self.username,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'balance': self.balance,
            'phone': self.phone,
            'password_hash': self.password_hash
        }

        return user_data

    def user_reg(self):
        user_data = {
            'username': self.username,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'balance': self.balance,
            'phone': self.phone
        }

        return user_data

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
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False, autoincrement=True)
    genre = db.Column(db.String(64), unique=True, nullable=False)
    type = db.Column(db.String(64), nullable=False)

    def genre_obj(self):
        genre_data = {
            'genre_id': self.id,
            'genre': self.genre,
            'type': self.type
        }

        # response = '<Genre %s>' %data
        # return repr(response)
        return genre_data

    def genre_reg(self):
        genre_data = {
            'genre': self.genre,
            'type': self.type
        }

        return genre_data


class Book(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    bookname = db.Column(db.String(64), nullable=False)
    image = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    genre = db.relationship('Genre', secondary='book_genre', lazy='subquery',
        backref=db.backref('books', lazy=True))

    def book_obj(self):
        book_data = {
            'book_id': self.id,
            'book_name': self.bookname,
            'image': self.image,
            'description': self.description,
        }

        # response = '<Book %s>' %data
        # return repr(response)
        return book_data

    def book_reg(self):
        book_data = {
            'book_name': self.bookname,
            'image': self.image,
            'description': self.description,
        }

        # response = '<Book %s>' %data
        # return repr(response)
        return book_data


class BookGenre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)

    def bookGenre_obj(self):
        bookGenre_data = {
            'bookCategory_id' : self.id,
            'genre_id': self.genre_id,
            'book_id': self.book_id,
        }

        return bookGenre_data

    def bookGenre_reg(self):
        bookGenre_data = {
            'genre_id': self.genre_id,
            'book_id': self.book_id,
        }

        return bookGenre_data

class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)

    def library_obj(self):
        library_data = {
            'lib_id': self.id,
            'user_id': self.user_id,
            'book_id': self.book_id
        }

        # response = '<Library %s>' %data
        # return repr(response)
        return library_data


# class RateComment(db.Model):
#     rate_comment_id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
#     book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
#     rate = db.Column(db.Integer, nullable=False)
#     comment = db.Column(db.Text, nullable=False)
#
#     def rateComment_obj(self):
#         rateComment_data = {
#             'rate_comment_id': self.rate_comment_id,
#             'book_id': self.book_id,
#             'rate': self.rate,
#             'comment': self.comment
#         }
#
#         response = '<Rate and Comment %s>' % data
#         return repr(response)
#         return rateComment_data