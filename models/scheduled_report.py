import calendar
from datetime import datetime

from celery_queue.tasks_queue import single_time_report_task
from models.ORM_handler import get_reports_for_time_frame, create_traffic_rows
from models.os_functions import program_ends


# ------------------------------------------------------------------------------------------------------
def check_weekly_date(send_date):
    week_day = send_date.weekday()
    today = datetime.today().weekday()
    return week_day == today


# ------------------------------------------------------------------------------------------------------
def check_monthly_date(send_date):
    day = send_date.day
    # need to check if the date <= max(date) in the current month , if not - need to handle
    max_days = calendar.monthrange(datetime.today().year, datetime.today().month)[1]
    return day <= max_days and day == datetime.today().day


# ------------------------------------------------------------------------------------------------------
def check_quarterly_date():
    get_first_day_of_the_quarter = datetime(datetime.today().year, 3 * ((datetime.today().month - 1) // 3) + 1, 1)
    return datetime.today() == get_first_day_of_the_quarter


# ------------------------------------------------------------------------------------------------------
def check_time_frame(time_frame):
    # get a list of the reports that need to run on the timeframe
    time_frame_reports = get_reports_for_time_frame(time_frame)
    if not time_frame_reports:
        program_ends()
    actual_reports = []
    for report in time_frame_reports:
        if time_frame == 'Daily':
            actual_reports.append(report)
        elif time_frame == 'Hourly':
            actual_reports.append(report)
        elif time_frame == 'Weekly' and check_weekly_date(report.first_send_date):
            actual_reports.append(report)
        elif time_frame == 'Monthly' and check_monthly_date(report.first_send_date):
            actual_reports.append(report)
        elif time_frame == 'Quarterly' and check_quarterly_date():
            actual_reports.append(report)
    return actual_reports


# ------------------------------------------------------------------------------------------------------
def run_scheduled_report(time_frame):
    # handle time_frame
    actual_reports = check_time_frame(time_frame)
    # create a traffic rows for each one of them
    if not actual_reports:
        program_ends()
    rows_data = create_traffic_rows(actual_reports)
    # run them as single time report
    for report in rows_data:
        # run_single_time_report(report[0], report[1])
        # calling to the tasks queue
        single_time_report_task.delay(report[0], report[1])


