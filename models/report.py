# ------------------------------------------------------------------------------------------------------

import logging
from datetime import datetime

from factories.factory import DeliveryMethodFactory, DataToFileFactory
from models import delivery_method_list, file_types_list
from models.ORM_handler import get_traffic_row_number, get_report_details, get_queries_details, \
    update_while_running_traffic_row
from models.os_functions import program_ends
from models.query import build_query
from models.timer import Timer

# setting logging variable -----------------------------------------------
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class Report:
    def __init__(self):
        self._traffic_row = None
        self._report_details = None
        self._timer = None
        self._delivery_method = None
        self._delivery_status = None
        self._report_duration = None
        self._execution_message = 'None'
        self._file_type = None
        self._queries = None
        self._folder_name = None

    # ------------------------------------------------------------------------------------------------------
    @property
    def traffic_row(self):
        return self._traffic_row

    @traffic_row.setter
    def traffic_row(self, row):
        self._traffic_row = row

    # ------------------------------------------------------------------------------------------------------
    @property
    def report_details(self):
        return self._report_details

    @report_details.setter
    def report_details(self, report_details):
        self._report_details = report_details

    # ------------------------------------------------------------------------------------------------------
    @property
    def timer(self):
        return self._timer

    @timer.setter
    def timer(self, value):
        self._timer = value

    # ------------------------------------------------------------------------------------------------------
    @property
    def delivery_method(self):
        return self._delivery_method

    @delivery_method.setter
    def delivery_method(self, delivery_method):
        self._delivery_method = delivery_method

    # ------------------------------------------------------------------------------------------------------
    @property
    def delivery_status(self):
        return self._delivery_status

    @delivery_status.setter
    def delivery_status(self, status):
        self._delivery_status = status

    # ------------------------------------------------------------------------------------------------------
    @property
    def execution_message(self):
        return self._execution_message

    @execution_message.setter
    def execution_message(self, message):
        self._execution_message = message

    # ------------------------------------------------------------------------------------------------------
    @property
    def file_type(self):
        return self._file_type

    @file_type.setter
    def file_type(self, file_type):
        self._file_type = file_type

    # ------------------------------------------------------------------------------------------------------

    @property
    def queries(self):
        return self._queries

    @queries.setter
    def queries(self, queries):
        self._queries = queries

    # ------------------------------------------------------------------------------------------------------
    @property
    def folder_name(self):
        return self._folder_name

    @folder_name.setter
    def folder_name(self, folder_name):
        self._folder_name = folder_name

    # ------------------------------------------------------------------------------------------------------
    def report_duration(self):
        self._timer.duration(datetime.now())
        return self._timer.duration

    def set_delivery_method_obj(self):
        try:
            log.info('set_delivery_method_obj')
            delivery_method_str = str(self.report_details.delivery_method).lower()
            if delivery_method_str in delivery_method_list:
                self.delivery_method = DeliveryMethodFactory.delivery_method_connection(delivery_method_str)
        except AssertionError as e:
            log.error(f'there was an error with set_delivery_method_obj method: {e}')
            self.update_report_state(status='failed', execution_message=e)
            program_ends()

    def set_file_type_obj(self):
        try:
            file_type_str = str(self.report_details.report_type).lower()
            if file_type_str in file_types_list:
                self.file_type = DataToFileFactory.get_file_handler(file_type_str)
        except AssertionError as e:
            log.error(f'there was an error with set_file_type_obj method: {e}')
            self.update_report_state(status='failed', execution_message=e)
            program_ends()

    def set_folder_name(self):
        if self.report_details.report_name != '':
            report_name_underline = str(self.report_details.report_name).replace(' ', '_')
            self.folder_name = 'report' + '_' + str(self.report_details.id) + '_' + report_name_underline
        else:
            empty_name = 'there was an error with set_folder_name method - report name is empty'
            log.error(empty_name)
            self.update_report_state(status='failed', execution_message=empty_name)
            program_ends()

    def set_queries(self):
        queries = []
        queries_list = get_queries_details(self)
        for query in queries_list:
            queries.append(build_query(self, query))
        self.queries = queries

    def report_validation(self):
        log.info('report_validation')
        try:
            assert self.traffic_row is not None
            assert self.traffic_row > 0
            assert self.report_details is not None
            assert len(self.queries) > 0
            for query in self.queries:
                assert len(query.query_content) > 0
        except AssertionError as e:
            log.error(f'there was an error with report_validation method: {e}')
            self.update_report_state(status='failed', execution_message=e)
            program_ends()

    def update_report_state(self, status, execution_message=None):
        log.info('update_report_state ' + status)
        if status == 'completed':
            self.timer.set_duration()
        self.delivery_status = status
        self.execution_message = execution_message
        update_while_running_traffic_row(self)

    # ------------------------------------------------------------------------------------------------------


def build_report(report_id, timestamp):
    log.info('build the report object')
    report = Report()
    report.traffic_row = get_traffic_row_number(report_id, timestamp)
    report.report_details = get_report_details(report_id)
    report.timer = Timer()
    report.set_delivery_method_obj()
    report.set_file_type_obj()
    report.set_folder_name()
    report.set_queries()
    log.info("build report object completed")
    return report
