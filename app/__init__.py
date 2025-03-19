from flask import Flask

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
 
    with app.app_context():
        from app.views import book_bp
        app.register_blueprint(book_bp)

    return app