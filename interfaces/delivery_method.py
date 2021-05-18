import abc
from abc import ABCMeta


# ------------------------------------------------------------------------------------------------------
class DeliveryMethod(metaclass=ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def send_report(report):
        """the connection interface"""
