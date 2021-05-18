import logging

from models.ORM_handler import create_traffic_rows
from models.os_functions import program_ends
from models.scheduled_report import check_time_frame
from models.single_time_report import run_single_time_report

# setting logging variable -----------------------------------------------
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


# single run tests -------------------------------------------------------

# report id = 7 - test on Vertica for two queries - different workbooks = excel - separate files
def single_run_time_test_1():
    report_id = 7
    timestamp = '2021-02-28 15:43:01'
    run_single_time_report(report_id, timestamp)
    log.info('test single_run_time_test 1 succeed')


# report id = 13 - test on Vertica for two queries - different workbooks = excel - multi tab
def single_run_time_test_2():
    report_id = 13
    timestamp = '2021-02-16 17:51:16'
    run_single_time_report(report_id, timestamp)
    log.info('test single_run_time_test 2 succeed')


# report id = 14 - test on MySql for two queries - different workbooks = excel - separate file
def single_run_time_test_3():
    report_id = 14
    timestamp = '2021-03-21 22:36:17'
    run_single_time_report(report_id, timestamp)
    log.info('test single_run_time_test 3 succeed')


# report id = 15 - test on MySql for two queries - different workbooks = excel - multi tab
def single_run_time_test_4():
    report_id = 15
    timestamp = '2021-03-21 22:37:03'
    run_single_time_report(report_id, timestamp)
    log.info('test single_run_time_test 4 succeed')


# report id = 16 - test on Vertica for one query - different workbooks = csv
def single_run_time_test_5():
    report_id = 16
    timestamp = '2021-03-21 22:40:03'
    run_single_time_report(report_id, timestamp)
    log.info('test single_run_time_test 5 succeed')


# scheduled run tests -------------------------------------------------------
def imitation_scheduled_run(time_frame):
    # handle time_frame
    actual_reports = check_time_frame(time_frame)
    # create a traffic rows for each one of them
    if not actual_reports:
        program_ends()
    rows_data = create_traffic_rows(actual_reports)
    return rows_data


# check specific report_id = 12
def scheduled_run_time_test_1():
    time_frame = 'Daily'
    rows_data = imitation_scheduled_run(time_frame)
    # run them as single time report
    for report in rows_data:
        if report[0] == 12:
            run_single_time_report(report[0], report[1])


single_run_time_test_1()
