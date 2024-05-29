# Yiğit Leblebicier 2012721035
# Fatma Yılmaz 2012721037
from flask import redirect, render_template, request, url_for, session
from os import path
from glob import glob
from enums import Routes
from trainers.regression import predict_with_model, load_model_metrics
from pandas import read_csv
import json


def get():
    models = glob(path.join("models", "*.pkl"))
    model_info = []
    for model_path in models:
        model_name = path.basename(model_path)
        metrics = load_model_metrics(model_path)
        model_info.append(
            {
                "name": model_name,
                "mse": metrics["mse"].__round__(2),
                "r2": metrics["r2"].__round__(2),
                "mape": metrics["mape"].__round__(2),
                "vif": metrics["vif"],
            }
        )

    result_file = session.get("predictions_file")
    result = None
    if result_file:
        with open(result_file, "r") as f:
            result = json.load(f)
        session["predictions_file"] = None

    return render_template(
        "predict.html",
        routes=[route.value for route in Routes],
        models=model_info,
        predictions=result,
    )


def post():
    model_name = request.form.get("select-model")
    predictions = predict_with_model(
        model_path=path.join("models", model_name),
        input=read_csv(request.files["select-input"]),
    )
    predictions_file = path.join("latest_predicts.json")
    with open(predictions_file, "w") as f:
        json.dump(predictions, f)
    session["predictions_file"] = predictions_file
    return redirect(url_for(".".join([Routes.PREDICT.value, "get"])))
