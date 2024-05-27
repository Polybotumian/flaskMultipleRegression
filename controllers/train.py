from flask import render_template, redirect, url_for, request, session
from os import path
from enums import Routes
from trainers.regression import multiple_linear_regression

def get():
    result_msg = session.get("result_msg")
    session["result_msg"] = None
    train_result = session.get("train_result")
    session["train_result"] = None
    return render_template(
        "train.html",
        routes=[route.value for route in Routes],
        result_msg=result_msg,
        train_result=train_result,
    )


def post():
    try:
        session["regression"] = request.form.get("select-regression")
        session["train_result"] = multiple_linear_regression(
            dataset_path=request.files["select-input"],
            save_path=path.join("models", request.form.get("new-model-name") + ".pkl"),
        )
        session["result_msg"] = "Model successfuly trained!"
    except Exception as e:
        session["result_msg"] = str(session["result_msg"])
    return redirect(url_for(".".join([Routes.TRAIN.value, get.__name__])))
