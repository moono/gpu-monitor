import json
import logging
import requests
from flask import Flask, render_template, jsonify


def load_json_data(config_file):
    with open(config_file) as f:
        config_dict = json.load(f)
    return config_dict


DEBUG_OVERRIDE = False
GPU_TEST_DATA = load_json_data('./gpu_debug_data.json')

# load server information
endpoints = load_json_data('./config.json')
usernames = load_json_data('./user_names.json')

# create flask instance
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = Flask(__name__)


def collect_once():
    chart_data_list = list()
    if DEBUG_OVERRIDE:
        for ii, chart_data in enumerate(GPU_TEST_DATA):
            chart_data_list.append(('moono_{:02d}'.format(ii), chart_data))
    else:
        # get all data from database
        for host_name, info in endpoints.items():
            try:
                r = requests.get('http://{:s}:{:s}/gpu_stat'.format(info['host'], info['port']))
                chart_data = r.json()
                chart_data_list.append((host_name, chart_data))
            except requests.exceptions.RequestException as e:
                pass

    return chart_data_list


@app.route('/')
def simple_homepage():
    initial_chart_data = collect_once()
    return render_template('index.html',
                           page_title='GPU-STATUS',
                           user_names=usernames,
                           initial_chart_data=initial_chart_data)


@app.route('/collect_all', methods=['GET'])
def collect_all_gpu_servers():
    chart_data = collect_once()
    return jsonify(chart_data)


# if __name__ == "__main__":
#     import os
#
#     app.debug = True
#     host = os.environ.get('IP', '0.0.0.0')
#     port = int(os.environ.get('PORT', 3033))
#     app.run(host=host, port=port)
