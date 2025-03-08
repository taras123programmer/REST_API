from flask import Flask
from app.config import Config

def create_app(config_class=Config):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config_class)
 
    with app.app_context():
        from app.views import book_bp
        app.register_blueprint(book_bp)

    return app