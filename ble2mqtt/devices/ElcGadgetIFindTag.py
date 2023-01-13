from datetime import datetime
import bluepy

from .basedevicetype import BaseDeviceType

class ElcGadgetIFindTag(BaseDeviceType):
    def __init__(self, addr, name):
        super().__init__(addr, name)
        self.manufacturer = '22000018'

    def fetch_battery_level(self, iface=0):
        connected = 0
        dev = bluepy.btle.Peripheral()
        try:
            dev.connect(self.addr, bluepy.btle.ADDR_TYPE_PUBLIC, iface)
            connected = 1
        except bluepy.btle.BTLEDisconnectError as e:
            print("Error connecting to {}: {}".format(self.addr, e))

        if connected:
            services = dev.getServices()
            print("Services are: {}".format(services))

        try:
            dev.disconnect()
        except bluepy.btle.BTLEDisconnectError as e:
            pass
        return None

    @classmethod
    def is_supported(cls, manufacturer, name):
        if manufacturer.startswith('220000') and name.startswith('IFind_'):
            return True
        return False
