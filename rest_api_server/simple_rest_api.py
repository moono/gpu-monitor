import os
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, jsonify
from flask_restful import Resource, Api

from nvidia_smi import run_nvidia_smi
from information_organizer import reorganize_and_merge_info_chartjs


parsed_gpu_info = None


def sensor():
    try:
        global parsed_gpu_info
        raw_info = run_nvidia_smi()
        parsed_gpu_info = reorganize_and_merge_info_chartjs(raw_info, parse_docker=True)
    except ValueError as e:
        print(e.message)
    return


sched_background = BackgroundScheduler(daemon=True)
sched_background.add_job(sensor, 'interval', seconds=1)
sched_background.start()


app = Flask(__name__)
api = Api(app)


class GPUStatus(Resource):
    def get(self):
        global parsed_gpu_info
        return jsonify(parsed_gpu_info)


api.add_resource(GPUStatus, '/gpu_stat')

if __name__ == '__main__':
    app.debug = True
    host = os.environ.get('IP', '0.0.0.0')
    port = int(os.environ.get('PORT', 3032))
    app.run(host=host, port=port)
