from flask import Flask

def create_app():
    app = Flask(__name__)

    # Konfigurasi aplikasi (opsional)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Registrasi Blueprint, jika ada
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
