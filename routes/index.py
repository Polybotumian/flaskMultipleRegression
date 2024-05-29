# Yiğit Leblebicier 2012721035
# Fatma Yılmaz 2012721037
from flask import Blueprint
from enums import Routes, Rules
from controllers.main import get

route = Blueprint(Routes.INDEX.value, __name__, template_folder=None)
route.add_url_rule(Rules.INDEX.value, view_func=get, methods=["GET"])
