import routes.index
from flask import Flask
import routes.index
import routes.predict
import routes.train
from os import environ, urandom
from base64 import b64encode

app = Flask("__name__")
app.secret_key = b64encode(urandom(12)).decode("utf-8")
app.register_blueprint(routes.index.route)
app.register_blueprint(routes.predict.route)
app.register_blueprint(routes.train.route)

if __name__ == "__main__":
    app.run(
        host=environ.get("FLASK_HOST", "127.0.0.1"),
        debug=environ.get("FLASK_DEBUG", False),
        port=environ.get("FLASK_PORT", 5000),
        load_dotenv=True,
    )
