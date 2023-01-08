from .ElcGadgetIFindTag import ElcGadgetIFindTag

class Devices(object):
    def __init__(self):
        self._other_devices = []
        self.watched_devices = {}

        self.supported_devices = [
            ElcGadgetIFindTag
        ]

    def other_devices(self, new_addr):
        self._other_devices = list(filter(lambda x:new_addr not in x, self._other_devices))
        self._other_devices.append(new_addr)

        if(len(self._other_devices) > 1000):
            self._other_devices = self._other_devices[1000:]

    def is_other_device(self, addr):
        if addr in self._other_devices:
            return True
        return False

    def manage(self, dev):
        if dev.addrType != 'public':
            # We key everything by hardware address, so can't cope with random addresses
            # so we just pretend these don't exist
            return

        if self.is_other_device(dev.addr):
            # Already seen it, it's not one of ours, so do no more
            return

        try:
            self.watched_devices[dev.addr].rssi(dev.rssi)
            #print("Device {} ({}), RSSI={} dB".format(dev.addr, dev.addrType, dev.rssi))
            return
        except KeyError:
            pass

        info = {}
        for (adtype, desc, value) in dev.getScanData():
            info[desc] = value

        try:
            for device in self.supported_devices:
                if device.is_supported(info['Manufacturer'], info['Complete Local Name']):
                    print("Found an ifind tag... {}".format(info['Complete Local Name']))
                    obj = device(dev.addr, info['Complete Local Name'])
                    self.watched_devices[dev.addr] = obj
                    return

            print("Found unsupported device Manufacturer: {} Name: {}".format(info['Manufacturer'], info['Complete Local Name']))
        except KeyError:
            pass

        self.other_devices(dev.addr)

    def each_supported_device(self):
        for device, obj in self.watched_devices.items():
            yield obj
