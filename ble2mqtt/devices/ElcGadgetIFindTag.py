from .basedevicetype import BaseDeviceType

# This device has these services and characteristics:
#
# Service UUID = 00001800-0000-1000-8000-00805f9b34fb
#  Characteristic[00002a00-0000-1000-8000-00805f9b34fb]: b'IFind_C5FD\x00'
#  Characteristic[00002a01-0000-1000-8000-00805f9b34fb]: 0000
#  Characteristic[00002a02-0000-1000-8000-00805f9b34fb]: 00
#  Characteristic[00002a04-0000-1000-8000-00805f9b34fb]: 08000a0000005802
# Service UUID = 00001801-0000-1000-8000-00805f9b34fb
#  Characteristic[00002a05-0000-1000-8000-00805f9b34fb]: 0100ffff
# Service UUID = 0000fff0-0000-1000-8000-00805f9b34fb
#  Characteristic[0000fff2-0000-1000-8000-00805f9b34fb] does not support read
#  Characteristic[0000fff1-0000-1000-8000-00805f9b34fb]: 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# Service UUID = 0000180a-0000-1000-8000-00805f9b34fb
# Service UUID = f000ffc0-0451-4000-b000-000000000000
#  Characteristic[f000ffc1-0451-4000-b000-000000000000] does not support read
#  Characteristic[f000ffc2-0451-4000-b000-000000000000] does not support read

class ElcGadgetIFindTag(BaseDeviceType):
    def __init__(self, addr, name):
        super().__init__(addr, name)
        self.manufacturer = '22000018'
        self.battery_uuid = None        # These devices do not support reading the battery

    @classmethod
    def is_supported(cls, manufacturer, name):
        if manufacturer.startswith('220000') and name.startswith('IFind_'):
            return True
        return False
