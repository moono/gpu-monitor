from apscheduler.schedulers.background import BackgroundScheduler
from nvidia_smi import run_nvidia_smi
from flask import Flask
from flask_restful import Resource, Api


parsed_gpu_info = None


def sensor():
    try:
        global parsed_gpu_info
        parsed_gpu_info = run_nvidia_smi()
    except ValueError as e:
        print(e.message)
    return


sched_background = BackgroundScheduler(daemon=True)
sched_background.add_job(sensor, 'interval', seconds=1)
sched_background.start()


app = Flask(__name__)
api = Api(app)


class GPUStatus(Resource):
    def post(self):
        global parsed_gpu_info
        # import pprint
        # pprint.pprint(parsed_gpu_info, width=1)
        return parsed_gpu_info


api.add_resource(GPUStatus, '/gpu_stat')

if __name__ == '__main__':
    app.run(debug=True)
