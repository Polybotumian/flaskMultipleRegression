# Yiğit Leblebicier 2012721035
# Fatma Yılmaz 2012721037
from flask import render_template
from enums import Routes

def get():
    return render_template("index.html", routes = [route.value for route in Routes])
