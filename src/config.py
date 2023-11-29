import pathlib
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_socketio import SocketIO


basedir = pathlib.Path(__file__).parent.resolve()
connex_app = connexion.App(__name__, specification_dir=basedir)

connex_app.app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'champions.db'}"
connex_app.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
connex_app.app.config["SECRET_KEY"] = "secret"



db = SQLAlchemy(connex_app.app)
ma = Marshmallow(connex_app.app)
connex_app.add_api(basedir / "swagger.yml")


CORS(connex_app.app, resources={r"/*":{"origins":"*"}})
connex_app.app.config['CORS_HEADERS'] = 'Content-Type'

socketio = SocketIO(connex_app.app, cors_allowed_origins="*")