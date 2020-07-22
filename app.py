from flask import Flask
from namespace.apiv1 import v1
from core.cache import cache
from flask_cors import CORS
import os

print(os.environ.get("REDIS_HOST", "host not found"))
print(os.environ.get("REDIS_PORT", "port not found"))

app = Flask(__name__)
CORS(app)
cache.init_app(app)
app.register_blueprint(v1)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
