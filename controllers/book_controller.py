from flask import jsonify, render_template, request

from app.forms import BookForm
from app.models import *


@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == "GET":
        book_list = Book.query.all()
        items = []
        for book in book_list:
            items.append({'book_name': book.bookname, 'img': book.image, 'desc': book.description})
        return jsonify(items), 200
    else:
        bookname = request.form.get('bookname')
        image = request.form.get('image')
        description = request.form.get('description')

        book = Book(bookname=bookname, image=image, description=description)
        db.session.add(book)
        db.session.commit()
        response = jsonify(book.book_reg())
        response.status_code = 200
        return response

#
# @app.route('/addBook', methods=['GET'])
# def addBookForm():
#     form = BookForm()
#     return render_template('addForm.html', form=form)


@app.route('/book/<book_id>', methods=['GET', 'DELETE'])
def book_info(book_id):
    book = Book.query.filter_by(id=book_id).first()
    if request.method == 'GET':
        response = jsonify(book.book_obj())
        response.status_code = 200
        return response
    elif request.method == 'DELETE':
        db.session.delete(book)
        db.session.commit()
        response = jsonify(book.book_obj())
        response.status_code = 200
        return response

# @app.route('/book', methods=['POST'])
# def addBook():
#     form = BookForm(request.form)
#     bookname = form.bookname.data
#     image = form.image.data
#     description = form.description.data
#
#     book = Book(bookname=bookname, image=image, description=description)
#     db.session.add(book)
#     db.session.commit()
#     return jsonify([{'book_name':bookname, 'image':image, 'description':description}])

