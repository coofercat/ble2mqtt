from datetime import datetime

class Metric(object):
    """ An item in the list of metrics stored by the device class """
    def __init__(self, val, timestamp=None):
        self.value = val
        if not timestamp:
            self.timestamp = datetime.now()
        else:
            self.timestamp = timestamp

class BaseDeviceType(object):
    """ This is a base class for all individual device classes """
    def __init__(self, addr, name):
        self.addr = addr
        self.manufacturer = '1234'
        self.name = name
        self.last_update = datetime.now()

        self.metrics = []

    def rssi(self, val):
        """ Insert an RSSI metric """
        self.metrics.append(Metric(val))
        self.last_update = datetime.now()

    def last_update_seconds_ago(self):
        """ Returns the fractional number of seconds since the last insert of a metric """
        diff = datetime.now() - self.last_update
        return diff.total_seconds()

    def average(self, clear=False):
        """ Returns the average of all the previous metrics, can optionally empty the local storage as it does so """
        accumilator = 0
        for item in self.metrics:
            accumilator = accumilator + item.value
        count = len(self.metrics)

        if clear:
            self.metrics = []
        try:
            return (accumilator / count, count)
        except ZeroDivisionError:
            return (None, 0)

    @classmethod
    def is_supported(cls, manufacturer, name):
        """ This class method should return True if the manufacturer/name are recognised """
        return False
