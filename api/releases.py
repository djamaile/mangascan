from flask_restx import Namespace, Resource, abort
from core.exceptions import RetrievingMangaException
from model.manga import manga
from core.cache import cache
from core import collect

api = Namespace("releases", description="get the newest manga releases")

api.models[manga.name] = manga

release_parser = api.parser()
release_parser.add_argument("date", type=str, location="args", required=False)


@api.route("/viz")
@api.param("date", "current date")
class VizReleases(Resource):
    @api.doc("Get the latest releases of viz")
    @api.marshal_with(manga, envelope="manga")
    @cache.cached(timeout=3600, query_string=True)
    def get(self):
        args = release_parser.parse_args()
        try:
            date = args["date"]
            viz_releases = collect.get_viz()
            return viz_releases
        except RetrievingMangaException as e:
            abort(e.status_code, e.error_message)


@api.route("/yenpress")
class YenPressReleases(Resource):
    @api.doc("Get the latest releases of yen press")
    @api.marshal_with(manga, envelope="manga")
    @cache.cached(timeout=3600, query_string=True)
    def get(self):
        try:
            yen_releases = collect.get_yen()
            return yen_releases
        except RetrievingMangaException as e:
            abort(e.status_code, e.error_message)


@api.route("/sevenseas")
class SevenSeasReleases(Resource):
    @api.doc("Get the latest releases of seven seas")
    @api.marshal_with(manga, envelope="manga")
    @cache.cached(timeout=3600, query_string=True)
    def get(self):
        try:
            ss_releases = collect.get_seven_seas()
            return ss_releases
        except RetrievingMangaException as e:
            abort(e.status_code, e.error_message)


@api.route("/darkhorse")
class DarkHorseReleases(Resource):
    @api.doc("Get the latest releases of dark horse")
    @api.marshal_with(manga, envelope="manga")
    @cache.cached(timeout=3600, query_string=True)
    def get(self):
        try:
            dark_releases = collect.get_dark_horse()
            return dark_releases
        except RetrievingMangaException as e:
            abort(e.status_code, e.error_message)


@api.route("/kodansha")
class KodanshaReleases(Resource):
    @api.doc("Get the latest releases of kodansha")
    @api.marshal_with(manga, envelope="manga")
    @cache.cached(timeout=3600, query_string=True)
    def get(self):
        try:
            kodansha_releases = collect.get_kodansha()
            return kodansha_releases
        except RetrievingMangaException as e:
            abort(e.status_code, e.error_message)
