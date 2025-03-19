from flask import current_app as app, Blueprint, jsonify, abort, request
from app.schemas import  BookSchema
from marshmallow.exceptions import  ValidationError

@app.route('/')
def main():
    return "Hello!"

book_bp = Blueprint('Book', 'book', url_prefix='/book')

books = [
    {'id':1,'title':'Book 1', 'author':'Author 1', 'text':'Text 1'},
    {'id':2,'title':'Book 2', 'author':'Author 2', 'text':'Text 2'},
    {'id':3,'title':'Book 3', 'author':'Author 3', 'text':'Text 3'},
    {'id':4,'title':'Book 4', 'author':'Author 4', 'text':'Text 4'}
]
last_id = 4

@book_bp.route('/<int:id>', methods=['GET'])
def get_book(id):
    res = [book for book in books if book['id'] == id]
    if res:
        book_schema = BookSchema()
        book = book_schema.dump(res[0])
        return jsonify(book)
    else:
        abort(404)

@book_bp.route('/', methods=['GET'])
def get_all_book():
    book_schema = BookSchema()
    books_list = [book_schema.dump(book) for book in books]
    return jsonify(books_list)

@book_bp.route('/', methods=['POST'])
def add_book():
    data = request.json
    book_schema = BookSchema()
    global last_id
    try:
        book = book_schema.load(data)
        last_id += 1
        book['id'] = last_id
        books.append(book)
    except ValidationError:
        abort(400)

    return '', 201

@book_bp.route('/<int:id>', methods=['DELETE'])
def delete_book(id):
    for b in books:
        if b['id'] == id:
            books.remove(b)
            return '', 204

    abort(404)

