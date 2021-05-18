import logging

from factories.factory import DbConnectionFactory
from models import limit_query_result, connection_type_list
from models.os_functions import program_ends

# setting logging variable -----------------------------------------------
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class Query:
    def __init__(self):
        self._queries_details = None
        self._connection_type = None
        self._query_content = None

    # ------------------------------------------------------------------------------------------------------
    @property
    def queries_details(self):
        return self._queries_details

    @queries_details.setter
    def queries_details(self, queries_details):
        self._queries_details = queries_details

    # ------------------------------------------------------------------------------------------------------
    @property
    def connection_type(self):
        return self._connection_type

    @connection_type.setter
    def connection_type(self, connection_type):
        self._connection_type = connection_type

    # ------------------------------------------------------------------------------------------------------
    @property
    def query_content(self):
        return self._query_content

    @query_content.setter
    def query_content(self, query_content):
        self._query_content = query_content

    # ------------------------------------------------------------------------------------------------------
    def check_limit(self):
        # handles the query limitation
        if 'limit' in self._query_content:
            query_arr = self._query_content.split("limit ")
            limit_num = int(query_arr[1])
            if limit_num > limit_query_result:
                self._query_content = self._query_content.replace(str(limit_num), str(limit_query_result))
        else:
            self._query_content = self._query_content + """ limit {}""".format(limit_query_result)

    def set_connection_type_obj(self, report):
        try:
            connection_type_str = str(self.queries_details.connection_type).lower()
            if connection_type_str in connection_type_list:
                self.connection_type = DbConnectionFactory.get_db_connection(connection_type_str)
        except AssertionError as e:
            log.error(f'there was an error with set_connection_type_obj method: {e}')
            report.update_report_state(status='failed', execution_message=e)
            program_ends()

    def set_query_content(self):
        self.query_content = self.queries_details.report_query

    # ------------------------------------------------------------------------------------------------------


def build_query(report, query):
    log.info('build the query object')
    query_instance = Query()
    query_instance.queries_details = query
    query_instance.set_connection_type_obj(report)
    query_instance.set_query_content()
    # query_instance.check_limit()
    log.info("build query object completed")
    return query_instance

