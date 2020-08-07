from quart import Quart, Blueprint
import asyncpg

app = Quart(__name__)

def create_app():
    app.config['SECRET_KEY'] = "9OLWxND4o83j4K4iuopO"
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
