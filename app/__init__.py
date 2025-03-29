from flask import Flask
from app.config import Config
from flask_sqlalchemy import  SQLAlchemy
from sqlalchemy.orm import  DeclarativeBase
from flask_migrate import  Migrate
from flask_restful import Api
from flasgger import  Swagger

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    api = Api(app)
    swagger = Swagger(app)

    from app.models import Book

    with app.app_context():
        from app.views import BookResource, BookByIdResource
        api.add_resource(BookResource, "/book/")
        api.add_resource(BookByIdResource, "/book/<int:book_id>")

    return app