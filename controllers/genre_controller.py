from flask import request, jsonify

from app.models import *


@app.route('/genre', methods=['GET', 'POST'])
def getAllGenre():
    if request.method == 'GET':
        genre_list = Genre.query.all()
        items = []
        for genre in genre_list:
            items.append({'genre': genre.genre, 'type': genre.type})
        return jsonify(items), 200
    else:
        gen = request.form.get('genre')
        type = request.form.get('type')

        genre =Genre(genre=gen, type=type)
        db.session.add(genre)
        db.session.commit()
        return jsonify(genre.genre_reg()), 200


@app.route('/genre/<genre_id>', methods=['GET', 'DELETE'])
def genre_info(genre_id):
    genre = Genre.query.filter_by(id=genre_id).first()
    if request.method == 'DELETE':
        db.session.delete(genre)
        db.session.commit()
    return jsonify(genre.genre_obj()), 200


@app.route('/genre/addbook/<genre_id>', methods=['POST'])
def add_book_genre(genre_id):
    book_id = request.form.get('book_id')
    genre_id= int(genre_id)

    book_g = BookGenre(book_id=book_id, genre_id=genre_id)
    db.session.add(book_g)
    db.session.commit()

    return jsonify(book_g.bookGenre_reg()), 200

#
# @app.route('/genre1/<category>', methods=['GET', 'POST'])
# def searchBookCategory(category):
#     book_id = request.form.get('id')
#     books = Book.query.get(book_id)
#     genre = Genre.query.get(category)
#     books.genre.append(genre)
#
#     db.session.add(books)
#     db.session.commit()