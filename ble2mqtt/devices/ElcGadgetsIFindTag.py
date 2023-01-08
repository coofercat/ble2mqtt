class Metric(object):
    def __init__(self, val, timestamp=None):
        self.value = val
        if not timestamp:
            self.timestamp = datetime.now()
        else:
            self.timestamp = timestamp

class ElcGadgetIFindTag(object):
    def __init__(self, addr, name):
        self.addr = addr
        self.manufacturer = '22000018'
        self.name = name
        self.last_update = datetime.now()

        self.metrics = []

    def rssi(self, val):
        self.metrics.append(Metric(val))
        self.last_update = datetime.now()

    def last_update_seconds_ago(self):
        diff = datetime.now() - self.last_update
        return diff.total_seconds()

    def average(self, clear=False):
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
        if manufacturer.startswith('220000') and name.startswith('IFind_'):
            return True
        return False
