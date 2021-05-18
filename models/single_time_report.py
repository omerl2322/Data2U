import logging

from models.os_functions import create_folder, program_ends
from models.report import build_report

# setting logging variable ---------------------------------------------------------------------------------------------
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def run_single_time_report(report_id, timestamp):
    report = build_report(report_id, timestamp)
    report.update_report_state('started')
    report.report_validation()
    create_folder(report)
    report.file_type.data_to_file(report)
    report.update_report_state('finished query')
    report.delivery_method.send_report(report)
    report.update_report_state('completed', 'completed without errors')
    log.info(f'run_single_time_report completed for report id - {report_id} and timestamp - {timestamp}')
    program_ends(report)


