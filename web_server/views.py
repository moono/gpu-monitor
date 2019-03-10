import os
import json
import requests
from flask import Flask, render_template, jsonify


def parse_config_file(config_file):
    with open(config_file) as f:
        config_dict = json.load(f)
    return config_dict


# load server information
endpoints = parse_config_file('./config.json')


# create flask instance
app = Flask(__name__)


def collect_once():
    # get all data from database
    chart_data_list = list()
    for host_name, info in endpoints.items():
        r = requests.get('http://{:s}:{:s}/gpu_stat'.format(info['host'], info['port']))
        chart_data_list.append((host_name, r.json()))

    return chart_data_list


@app.route('/')
def simple_homepage():
    initial_chart_data = collect_once()
    return render_template('index.html',
                           page_title='GPU-STATUS',
                           initial_chart_data=initial_chart_data)


@app.route('/collect_all', methods=['GET'])
def collect_all_gpu_servers():
    chart_data = collect_once()
    return jsonify(chart_data)


if __name__ == "__main__":
    app.debug = True
    host = os.environ.get('IP', '0.0.0.0')
    port = int(os.environ.get('PORT', 3033))
    app.run(host=host, port=port)
