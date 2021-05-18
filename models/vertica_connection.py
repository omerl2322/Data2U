import logging

import vertica_python

from interfaces.db_connection import Connection
# ------------------------------------------------------------------------------------------------------
from models import vertica_connection_json

# setting logging variable -----------------------------------------------
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class VerticaConnection(Connection):

    def __init__(self):
        self.host = vertica_connection_json['host']
        self.port = vertica_connection_json['port']
        self.database = vertica_connection_json['database']
        self.user = vertica_connection_json['user']
        self.password = vertica_connection_json['password']

    def get_connection(self):
        return {'host': self.host, 'port': self.port, 'database': self.database, 'user': self.user,
                'password': self.password}

    def run_query(self, query_content):
        log.info('run_query: vertica connection')
        try:
            conn_info = self.get_connection()
            connection = vertica_python.connect(**conn_info)
            cur = connection.cursor()
            cur.execute(query_content)
            temp_result = cur.fetchall()
            column_list = [d.name for d in cur.description]
            return temp_result, column_list
        except vertica_python.errors.Error as err:
            log.error(f'there was an error with run_query method on vertica connection : {err}')
            raise RuntimeError(err)
# ------------------------------------------------------------------------------------------------------
