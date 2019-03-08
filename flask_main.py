# encoding: utf-8

from flask import Flask
from flask import render_template
from data_analyze import get_daily_usage

app = Flask(__name__)


@app.route('/')
def index():
    key_usage_data = get_daily_usage()
    return render_template("index.html", keyUsageData=key_usage_data)


app.run(host="127.0.0.1", port=5555, debug=True)
