from flask import Blueprint
from enums import Routes, Rules
from controllers.train import get, post

route = Blueprint(Routes.TRAIN.value, __name__, template_folder=None)
route.add_url_rule(Rules.TRAIN.value, view_func=get, methods=["GET"])
route.add_url_rule("/train/post", view_func=post, methods=["POST"])
