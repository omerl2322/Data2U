import abc
from abc import ABCMeta


# ------------------------------------------------------------------------------------------------------
class Connection(metaclass=ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def get_connection():
        """the connection interface"""

    @staticmethod
    @abc.abstractmethod
    def run_query(query_content):
        """the connection interface"""
