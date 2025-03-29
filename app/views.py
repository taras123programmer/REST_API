from flask import jsonify, request, abort, Response
from flask_restful import Resource
from app import db
from app.models import Book
from app.schemas import BookSchema
from marshmallow.exceptions import ValidationError

class BookResource(Resource):
    """
    This is the Book resource
    ---
    tags:
      - Book
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The book ID
    responses:
      200:
        description: Book details
        schema:
          id: Book
          properties:
            id:
              type: integer
              description: The book ID
              example: 1
            title:
              type: string
              description: The book title
              example: "Flask for Beginners"
            author:
              type: string
              description: The author of the book
              example: "John Doe"
            text:
              type: string
              description: The content/text of the book
              example: "This is the content of the book."
    """

    def get(self):
        """
        Get a specific book or all books
        ---
        description: Get a book by ID or get all books if no ID is provided.
                     Supports pagination with cursor and limit.
        tags:
            - Book
        parameters:
          - name: limit
            in: query
            type: integer
            required: false
            description: The number of books to return (default is 10)
            example: 10
          - name: cursor
            in: query
            type: integer
            required: false
            description: The ID to start pagination from (default is the first book)
            example: 5
        responses:
          200:
            description: A single book or a list of books
            schema:
              type: array
              items:
                id: Book
                properties:
                  title:
                    type: string
                    description: The book title
                    example: "Flask for Beginners"
                  author:
                    type: string
                    description: The author of the book
                    example: "John Doe"
                  text:
                    type: string
                    description: The content/text of the book
                    example: "This is the content of the book."
        """
        if 'limit' in request.args:
            limit = int(request.args['limit'])
        else:
            limit = 10

        if 'cursor' in request.args:
            cursor = request.args['cursor']
            books = db.session.query(Book).filter(Book.id > cursor).limit(limit).all()
        else:
            books = db.session.query(Book).limit(limit).all()

        if not books:
            abort(404)

        cursor = books[-1].id

        book_schema = BookSchema()
        res = {'books': [book_schema.dump(book) for book in books], 'cursor': cursor}
        return jsonify(res)

    def post(self):
        """
    This is the Book resource
    ---
    tags:
      - Book
    parameters:
      - name: body
        in: body
        required: true
        description: The data for creating a book
        schema:
          type: object
          properties:
            title:
              type: string
              example: "My Book"
            author:
              type: string
              example: "John Doe"
            text:
              type: string
              example: "This is the content of the book."
    responses:
      201:
        description: Book created successfully
        schema:
          id: Book
          properties:
            id:
              type: integer
              description: The book ID
              example: 1
            title:
              type: string
              description: The book title
              example: "My Book"
            author:
              type: string
              description: The author of the book
              example: "John Doe"
            text:
              type: string
              description: The content of the book
       """
        data = request.get_json()
        book_schema = BookSchema()
        try:
            book_dict = book_schema.load(data)
            book = Book(
                title=book_dict['title'],
                author=book_dict['author'],
                text=book_dict['text']
            )
            db.session.add(book)
            db.session.commit()

        except ValidationError:
            abort(400)

        return Response(status=201)


class BookByIdResource(Resource):
    """
           Get a book by ID
           ---
           description: Get a specific book by its ID
           parameters:
             - name: book_id
               in: path
               type: integer
               required: true
               description: The book ID (mandatory in the URL path)
           responses:
             200:
               description: The book
               schema:
                 id: Book
                 properties:
                   id:
                     type: integer
                     description: The book ID
                     example: 1
                   title:
                     type: string
                     description: The book title
                     example: "Flask for Beginners"
                   author:
                     type: string
                     description: The author of the book
                     example: "John Doe"
                   text:
                     type: string
                     description: The content of the book
                     example: "This is the content of the book."
           """

    def get(self, book_id):
        """
        Get a specific book by ID
        ---
        tags:
            - Book
        description: Get a book by ID
        parameters:
          - name: book_id
            in: path
            type: integer
            required: true
            description: The book ID
        responses:
          200:
            description: A single book
            schema:
              id: Book
              properties:
                id:
                  type: integer
                  description: The book ID
                  example: 1
                title:
                  type: string
                  description: The book title
                  example: "Flask for Beginners"
                author:
                  type: string
                  description: The author of the book
                  example: "John Doe"
                text:
                  type: string
                  description: The content/text of the book
                  example: "This is the content of the book."
        """
        book = db.session.query(Book).filter_by(id=book_id).first()
        if book:
            book_schema = BookSchema()
            book = book_schema.dump(book)
            return jsonify(book)
        else:
            abort(404)

    def delete(self, book_id: int):
        """
        Delete a book by ID
        ---
        tags:
            - Book
        description: Delete a specific book by its ID
        parameters:
          - name: book_id
            in: path
            type: integer
            required: true
            description: The book ID to be deleted
        responses:
          204:
            description: Book successfully deleted
        """
        book = db.session.query(Book).filter_by(id=book_id).first()
        if book:
            db.session.delete(book)
            db.session.commit()
            return '', 204
        else:
            abort(404)
