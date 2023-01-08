from datetime import datetime

from .basedevicetype import BaseDeviceType

class ElcGadgetIFindTag(BaseDeviceType):
    def __init__(self, addr, name):
        super().__init__(addr, name)
        self.manufacturer = '22000018'

    @classmethod
    def is_supported(cls, manufacturer, name):
        if manufacturer.startswith('220000') and name.startswith('IFind_'):
            return True
        return False
