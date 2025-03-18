from app import db

class Book(db.Model):
    __tablename__ = "Book"

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    title = db.Column(db.String(30), nullable=False)
    author = db.Column(db.String(30), nullable=False)
    text = db.Column(db.Text, nullable=False)