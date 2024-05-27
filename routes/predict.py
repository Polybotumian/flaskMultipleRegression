from flask import Blueprint
from enums import Routes, Rules
from controllers.predict import get, post

route = Blueprint(Routes.PREDICT.value, __name__, template_folder=None)
route.add_url_rule(Rules.PREDICT.value, view_func=get, methods=["GET"])
route.add_url_rule(Rules.PREDICT.value, view_func=post, methods=["POST"])
