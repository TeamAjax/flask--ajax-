from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    role = db.Column(db.String(20), index=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        user_data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'password_hash': self.password_hash,
        }

        return user_data



    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# class user(db.Model):
#     user_id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
#     username = db.Column(db.String(64), index=True, unique=True, nullable=False)
#     firstname = db.Column(db.String(64), nullable=False)
#     lastname = db.Column(db.String(64), nullable=False)
#     email = db.Column(db.String(120), index=True, unique=True, nullable=False)
#     balance = db.Column(db.Float)
#     phone = db.Column(db.Integer, nullable=False)
#     password_hash = db.Column(db.String(128), nullable=False)
#     # posts = db.relationship('Post', backref='author', lazy='dynamic')
#
#     def __repr__(self):
#         data = {
#             'user_id': self.user_id,
#             'username': self.username,
#             'firstname': self.firstname,
#             'lastname': self.lastname,
#             'email': self.email,
#             'balance': self.balance,
#             'phone': self.phone,
#             'password_hash': self.password_hash
#         }
#
#         response = '<User %s>' %data
#         return repr(response)
#
#
# class genre(db.Model):
#     genre_id =  db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
#     genre = db.Column(db.String(64), unique=True, nullable=False)
#     type = db.Column(db.String(64), nullable=False)
#
#     def __repr__(self):
#         data = {
#             'Genre ID': self.genre_id,
#             'Genre': self.genre,
#             'Type': self.type
#         }
#
#         response = '<Genre %s>' %data
#         return repr(response)
#
# class book(db.Model):
#     book_id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
#     bookname = db.Column(db.String(64), nullable=False)
#     image = db.Column(db.BLOB, nullable=False)
#     description = db.Column(db.String(64), nullable=False)
#
#     def __repr__(self):
#         data = {
#             'Book ID': self.book_id,
#             'Book Name': self.bookname,
#             'Image': self.image,
#             'Description': self.description
#         }
#
#         response = '<Book %s>' %data
#         return repr(response)
#
# class library(db.Model):
#     lib_id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
#     gen_id = db.Column(db.Integer, db.ForeignKey('genre.genre_id'), nullable=False)
#     bo_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), nullable=False)
#     bo_name = db.Column(db.Integer, db.ForeignKey('book.bookname'), nullable=False)
#
#     def __repr__(self):
#         data = {
#             'Library ID': self.lib_id,
#             'Genre ID': self.gen_id,
#             'Book ID': self.bo_id,
#             'Book Name': self.bo_name
#         }
#
#         response = '<Library %s>' %data
#         return repr(response)
#
#     class rateComment(db.Model):
#         book_id1 = db.Column(db.Integer, db.ForeignKey('book.book_id'))
#         rate = db.Column(db.Integer, nullable=False)
#         comment = db.Column(db.Text, nullable=False)
#
#         def __repr__(self):
#             data = {
#                 'Book ID': self.book_id1,
#                 'Rate': self.rate,
#                 'Comment': self.comment
#             }
#
#             response = '<Rate and Comment %s>' % data
#             return repr(response)