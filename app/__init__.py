from flask import Flask
from app.config import Config
from flask_sqlalchemy import  SQLAlchemy
from sqlalchemy.orm import  DeclarativeBase
from flask_migrate import  Migrate

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.models import Book

    with app.app_context():
        from app.views import book_bp
        app.register_blueprint(book_bp)

    return app