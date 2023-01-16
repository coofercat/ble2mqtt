from datetime import datetime
import bluepy

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

        self.battery = None
        self.battery_cache_time = datetime.now()
        self.battery_cache_ttl = 600

        # Not all devices can support this UUID, but if they do, we can fetch battery levels easily
        self.battery_uuid = 0x180f

        self.metrics = []

    def rssi(self, val):
        """ Insert an RSSI metric """
        self.metrics.append(Metric(val))
        self.last_update = datetime.now()

    def _disconnect_ble(self, device):
        """ Disconnect, even if not really connected ;-) """
        if device is None:
            return
        try:
            device.disconnect()
        except bluepy.btle.BTLEDisconnectError as e:
            pass

    def fetch_battery_level(self, iface=0):
        """ Immediately connect to a device, get its battery level and return it """
        if self.battery_uuid is None:
            # This device does not support reading the battery level
            return None
        battery = None
        dev = bluepy.btle.Peripheral()
        try:
            dev.connect(self.addr, bluepy.btle.ADDR_TYPE_PUBLIC, iface)
        except bluepy.btle.BTLEDisconnectError as e:
            #print("Error connecting to {}: {}".format(self.addr, e))
            return None

        try:
            service = dev.getServiceByUUID(self.battery_uuid)
        except bluepy.btle.BTLEGattError:
            # battery service not found
            self._disconnect_ble(dev)
            return None

        char = getCharacteristics()[0]
        val = char.read()
        battery = int.from_bytes(val, byteorder='little', signed=True)

        self._disconnect_ble(dev)
        return battery

    def battery_level(self):
        """ Return a cached measurment of the battery level of the device """
        """ Fetching battery takes time and effort, so cache the result """
        """ and only re-fetch it if necessary """
        diff = datetime.now() - self.battery_cache_time
        if diff.total_seconds() > self.battery_cache_ttl:
            self.battery = self.fetch_battery_level()
            self.battery_cache_time = datetime.now()

        return self.battery

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
