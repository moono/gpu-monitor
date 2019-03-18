import os
import json
import logging
import requests
from flask import Flask, render_template, jsonify

DEBUG_OVERRIDE = False
GPU_TEST_DATA = [
    {
        "bar_chart": {
            "labels": ["gpu_0", "gpu_1"],
            "memory_data": [95, 55],
            "utilization_data": [90, 98]
        },
        "pie_chart": {
            "labels": [
                "gpu_0/Xorg_dakdmksadlmaskl_dmskmals_am",
                "gpu_0/compiz",
                "gpu_0/chrome",
                "gpu_1/Xorg",
                "gpu_1/compiz",
                "gpu_1/chrome",
                "free"
            ],
            "processes_data": [
                347,
                68,
                46,
                347,
                68,
                46,
                7648
            ]
        }
    },
    {
        "bar_chart": {
            "labels": ["gpu_0", "gpu_1", "gpu_2", "gpu_3"],
            "memory_data": [95, 55, 95, 55],
            "utilization_data": [90, 98, 90, 98]
        },
        "pie_chart": {
            "labels": [
                "gpu_0/Xorg",
                "gpu_1/compiz",
                "gpu_2/chrome",
                "gpu_3/Xorg",
                "free"
            ],
            "processes_data": [
                347,
                68,
                46,
                347,
                7648
            ]
        }
    },
    {
        "bar_chart": {
            "labels": ["gpu_0", "gpu_1", "gpu_2", "gpu_3", "gpu_4", "gpu_5"],
            "memory_data": [95, 55, 95, 55, 95, 55],
            "utilization_data": [90, 98, 90, 98, 90, 98]
        },
        "pie_chart": {
            "labels": [
                "gpu_0/Xorg",
                "gpu_1/compiz",
                "gpu_2/chrome",
                "gpu_3/Xorg",
                "gpu_4/chrome",
                "gpu_5/Xorg",
                "free"
            ],
            "processes_data": [
                347,
                68,
                46,
                347,
                46,
                347,
                7648
            ]
        }
    },
    {
        "bar_chart": {
            "labels": ["gpu_0", "gpu_1", "gpu_2", "gpu_3", "gpu_4", "gpu_5", "gpu_6", "gpu_7"],
            "memory_data": [95, 55, 95, 55, 95, 55, 95, 55],
            "utilization_data": [90, 98, 90, 98, 90, 98, 90, 98]
        },
        "pie_chart": {
            "labels": [
                "gpu_0/Xorg",
                "gpu_1/compiz",
                "gpu_2/chrome",
                "gpu_3/Xorg",
                "gpu_4/chrome",
                "gpu_5/Xorg",
                "gpu_6/compiz",
                "gpu_7/chrome",
                "free"
            ],
            "processes_data": [
                347,
                68,
                46,
                347,
                46,
                347,
                46,
                347,
                7648
            ]
        }
    }
]


def parse_config_file(config_file):
    with open(config_file) as f:
        config_dict = json.load(f)
    return config_dict


# load server information
endpoints = parse_config_file('./config.json')
usernames = parse_config_file('./user_names.json')

# create flask instance
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = Flask(__name__)


def create_more_chart_data(bar_pie_chart_data):
    bar_chart = bar_pie_chart_data['bar_chart']
    pie_chart = bar_pie_chart_data['pie_chart']

    merged_chart_data = {
        'bar_chart': bar_chart,
        'pie_chart': pie_chart,
    }
    labels = bar_chart['labels']
    for gpu_label in labels:
        data_label = list()
        memory_data = list()
        for process_label, process_data in zip(pie_chart['labels'], pie_chart['processes_data']):
            prefix_n_name = process_label.split('/', 1)

            if prefix_n_name[0] == gpu_label:
                data_label.append(prefix_n_name[1])
                memory_data.append(process_data)

        merged_chart_data[gpu_label] = {
            'labels': data_label,
            'memory_data': memory_data,
        }
    return merged_chart_data


def collect_once():
    chart_data_list = list()
    if DEBUG_OVERRIDE:
        for ii, test_data in enumerate(GPU_TEST_DATA):
            chart_data = create_more_chart_data(test_data)
            chart_data_list.append(('moono_{:02d}'.format(ii), chart_data))
    else:
        # get all data from database
        for host_name, info in endpoints.items():
            r = requests.get('http://{:s}:{:s}/gpu_stat'.format(info['host'], info['port']))

            bar_pie_chart_data = r.json()
            chart_data = create_more_chart_data(bar_pie_chart_data)
            chart_data_list.append((host_name, chart_data))

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


if __name__ == "__main__":
    app.debug = True
    host = os.environ.get('IP', '0.0.0.0')
    port = int(os.environ.get('PORT', 3033))
    app.run(host=host, port=port)
