from flask import current_app as app, Blueprint, jsonify, abort, request
from app.schemas import  BookSchema
from marshmallow.exceptions import  ValidationError
from app import db
from app.models import Book

@app.route('/')
def main():
    return "Hello!"

book_bp = Blueprint('Book', 'book', url_prefix='/book')

@book_bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = db.session.query(Book).filter_by(id=book_id).first()
    if book:
        book_schema = BookSchema()
        book = book_schema.dump(book)
        return jsonify(book)
    else:
        abort(404)

@book_bp.route('/', methods=['GET'])
def get_all_book():
    if 'limit' in request.args :
        limit = int(request.args['limit'])
    else:
        limit = 10

    if 'cursor' in request.args:
        cursor = request.args['cursor']
        books = (db.session.query(Book).filter(Book.id > cursor).limit(limit).all())
    else:
        books = db.session.query(Book).all()

    if not books:
        abort(404)
    cursor = books[-1].id

    book_schema = BookSchema()
    res = {'books': [book_schema.dump(book) for book in books], 'cursor' : cursor}
    return jsonify(res)

@book_bp.route('/', methods=['POST'])
def add_book():
    data = request.json
    book_schema = BookSchema()
    try:
        book_dict = book_schema.load(data)
        book = Book(title=book_dict['title'], author=book_dict['author'], text=book_dict['text'])
        db.session.add(book)
        db.session.commit()

    except ValidationError:
        abort(400)

    return '', 201

@book_bp.route('/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = db.session.query(Book).filter_by(id=book_id).first()
    if book:
        db.session.delete(book)
        db.session.commit()
        return '', 201

    else:
        abort(404)