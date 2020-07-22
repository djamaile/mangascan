from flask_restx import Api
from api.releases import api
from flask import Blueprint

v1 = Blueprint("api", __name__, url_prefix="/api/v1")
api_v1 = Api(
    v1,
    title="Manga Scan",
    version="0.1",
    description="See the newest manga releases from different publishers",
)
api_v1.add_namespace(api)
