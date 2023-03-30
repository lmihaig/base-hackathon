from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_cors import CORS
from apis import api

app = Flask(__name__)
CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"
app.wsgi_app = ProxyFix(app.wsgi_app)
api.init_app(app)


if __name__ == "__main__":
    app.run(debug=True, port=8069, host="0.0.0.0")
