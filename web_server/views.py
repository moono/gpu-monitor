import os
import json
import logging
import requests
from flask import Flask, render_template, jsonify


def parse_config_file(config_file):
    with open(config_file) as f:
        config_dict = json.load(f)
    return config_dict


# load server information
endpoints = parse_config_file('./config.json')


# create flask instance
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = Flask(__name__)


def collect_once():
    # get all data from database
    chart_data_list = list()
    for host_name, info in endpoints.items():
        r = requests.get('http://{:s}:{:s}/gpu_stat'.format(info['host'], info['port']))

        bar_pie_chart_data = r.json()
        chart_data = create_n_merge_stacked_bar_chart_data(bar_pie_chart_data)
        chart_data_list.append((host_name, chart_data))

    return chart_data_list


def create_n_merge_stacked_bar_chart_data(bar_pie_chart_data):
    bar_chart = bar_pie_chart_data['bar_chart']
    pie_chart = bar_pie_chart_data['pie_chart']

    labels = bar_chart['labels']
    datasets = list()
    for gpu_label in labels:
        data_label = list()
        memory_data = list()
        for process_label, process_data in zip(pie_chart['labels'], pie_chart['processes_data']):
            prefix_n_name = process_label.split('/', 1)

            if prefix_n_name[0] == gpu_label:
                data_label.append(prefix_n_name[1])
                memory_data.append(process_data)

        datasets.append({
            'label': data_label,
            'data': memory_data
        })

    merged_chart_data = {
        'bar_chart': bar_chart,
        'pie_chart': pie_chart,
        'stacked_chart': {
            'labels': labels,
            'datasets': datasets
        }
    }

    return merged_chart_data


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
