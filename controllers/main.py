from flask import render_template
from enums import Routes

def get():
    return render_template("index.html", routes = [route.value for route in Routes])
