import logging

from models.csv_file_handler import CsvFile
from models.email_handler import ViaEmail
from models.excel_file_handler import ExcelMultiTab, ExcelSeparateFiles
from models.html_file_handler import HTMLFile
from models.mysql_connection import MySqlConnection
from models.slack_handler import ViaSlack
from models.vertica_connection import VerticaConnection

# setting logging variable ---------------------------------------------------------------------------------------------
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


# ------------------------------------------------------------------------------------------------------
class DataToFileFactory:
    # ['Excel - Multi Tab', 'CSV', 'HTML', 'Excel - Separate Files']
    @staticmethod
    def get_file_handler(file_type):
        files_dictionary = {
            'excel - multi tab': ExcelMultiTab,
            'excel - separate files': ExcelSeparateFiles,
            'csv': CsvFile,
            'html': HTMLFile
        }
        if file_type in files_dictionary.keys():
            return files_dictionary[file_type]()
        else:
            raise AssertionError("file_handler not found")


# ------------------------------------------------------------------------------------------------------
class DeliveryMethodFactory:
    @staticmethod
    def delivery_method_connection(delivery_type):
        delivery_dictionary = {
            'email': ViaEmail,
            'slack': ViaSlack
        }
        log.info('delivery_method_connection')
        if delivery_type in delivery_dictionary.keys():
            return delivery_dictionary[delivery_type]()
        else:
            raise AssertionError("delivery_method not found")


# ------------------------------------------------------------------------------------------------------
class DbConnectionFactory:
    @staticmethod
    def get_db_connection(db_type):
        db_dictionary = {
            'vertica': VerticaConnection,
            'mysql': MySqlConnection
        }
        log.info('get_db_connection')
        if db_type in db_dictionary.keys():
            return db_dictionary[db_type]()
        else:
            raise AssertionError("db not found")
