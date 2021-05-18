import logging
from datetime import datetime

from flask import Flask, send_from_directory, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint

from app import time_frames
from celery_queue.tasks_queue import single_time_report_task
# change the web server to gunicron
from models.scheduled_report import run_scheduled_report

# setting up flask -------------------------------------------------------
app = Flask(__name__)
# setting logging variable -----------------------------------------------
# root_logger = logging.getLogger()
# log_level = obpython.settings.get("automl.log_level", "INFO")
# root_logger.setLevel(log_level)
# console_handler = logging.StreamHandler()
# formatter = obpython.logging.OBJsonFormatter(None)
# console_handler.setFormatter(formatter)
# root_logger.addHandler(console_handler)

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


# swagger ---------------------------------------------------------------
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "New Push Report tool"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)


# routes ----------------------------------------------------------------

@app.route("/")
def index():
    return return_status_code("The server is up", 200)


@app.route('/single_time_report', methods=["GET", "POST"])
def single_time_report():
    # store the variables from the http call
    report_id = request.args.get('report_id')
    timestamp = request.args.get('timestamp')
    if check_input(report_id, timestamp):
        log.info('input ok, sending report to task queue')
        single_time_report_task.delay(report_id, timestamp)
        return return_status_code("I got the report, running report id :" + report_id, 200)


@app.route('/scheduled_report', methods=["GET", "POST"])
def scheduled_report():
    time_frame = request.args.get('time_frame')
    if check_time_frame(time_frame):
        log.info('time frame ok, running the scheduled report process')
        run_scheduled_report(time_frame)
        return return_status_code("Runs reports for time frame:" + time_frame, 200)


def return_status_code(message, status_code):
    return jsonify(message=message), status_code


# input check -----------------------------------------------------------

def check_time_frame(time_frame):
    if time_frame in time_frames:
        return True
    else:
        log.error('issue with time_frame string: %s', time_frame)
        return return_status_code("The time_frame should be one of:" + time_frames, 422)


def check_input(report_id, timestamp):
    date_time_format = '%Y-%m-%d %H:%M:%S'
    report_num = report_id.isnumeric()
    try:
        timestamp_datetime = datetime.strptime(timestamp, date_time_format)
        if isinstance(report_num, int) and isinstance(timestamp_datetime, datetime):
            return True
    except Exception as message:
        log.error('issue with report input: %s', message)
        return return_status_code(message, 422)


# main -----------------------------------------------------------


if __name__ == '__main__':
    app.run(port=8000)
