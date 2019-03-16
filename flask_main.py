# encoding: utf-8

import os
import ujson
from flask import Flask
from flask import jsonify
from flask import render_template
from data_analyze import *
from datetime import timedelta

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = timedelta(seconds=1)


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/keyboard_usage_data")
def keyboard_usage_data():
    cache_seconds = 100
    file_name = "data/cache.json"
    if os.path.exists(file_name) and time.time() - os.stat(file_name).st_mtime <= cache_seconds:
        with open(file_name) as fd:
            res = ujson.load(fd)
    else:
        raw_data = get_raw_data()
        daily_log_time_each_key, daily_log_time = get_daily_log_time(raw_data)
        daily_press_time_each_key, daily_press_time = get_daily_total_press_time(raw_data)
        res = {
            "daily_log_time": daily_log_time,
            "daily_log_time_each_key": daily_log_time_each_key,
            "daily_press_time": daily_press_time,
            "daily_press_time_each_key": daily_press_time_each_key
        }
        with open(file_name, "w") as fd:
            ujson.dump(res, fd)
    return jsonify(res)


app.run(host="127.0.0.1", port=5555, debug=True)
