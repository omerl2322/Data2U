from datetime import datetime


class Timer:
    def __init__(self):
        self._start_time = datetime.now()
        self._duration = None

    @property
    def start_time(self):
        return self._start_time

    @property
    def duration(self):
        return self._duration

    def set_duration(self):
        self._duration = (datetime.now() - self.start_time).seconds
