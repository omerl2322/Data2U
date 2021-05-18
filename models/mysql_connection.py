import mysql.connector
import logging
from interfaces.db_connection import Connection
# ------------------------------------------------------------------------------------------------------
from models import mysql_connection_json

# setting logging variable -----------------------------------------------
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class MySqlConnection(Connection):

    def __init__(self):
        self.host = mysql_connection_json['host']
        self.port = mysql_connection_json['port']
        self.database = mysql_connection_json['database']
        self.user = mysql_connection_json['user']
        self.password = mysql_connection_json['password']

    # ------------------------------------------------------------------------------------------------------
    def get_connection(self):
        return {'host': self.host, 'port': self.port, 'database': self.database, 'user': self.user,
                'password': self.password}

    # ------------------------------------------------------------------------------------------------------
    def run_query(self, query_content):
        log.info('run_query: mysql connection')
        try:
            conn_info = self.get_connection()
            connection = mysql.connector.connect(**conn_info)
            cursor = connection.cursor()
            cursor.execute(query_content)
            temp_result = cursor.fetchall()
            column_list = [i[0] for i in cursor.description]
            return temp_result, column_list
        except mysql.connector.Error as err:
            log.error(f'there was an error with run_query method on mysql connection : {err}')
            raise RuntimeError(err)
