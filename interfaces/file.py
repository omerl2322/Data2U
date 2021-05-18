import abc
import base64
from abc import ABCMeta


# ------------------------------------------------------------------------------------------------------
class File(metaclass=ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def data_to_file(report):
        """the file interface"""

    @staticmethod
    def file_encode(file_name):
        with open(file_name, 'rb') as f:
            data = f.read()
            f.close()
        encoded = base64.b64encode(data).decode()
        return encoded
