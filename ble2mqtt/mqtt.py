import paho.mqtt.client
import paho.mqtt.publish

class Mqtt(object):
    def __init__(self, client='ble2mqtt'):
        self.hostname = 'localhost'
        self.port = 1884
        self.client_id = client
        self.keepalive = 60
        self.will = None
        self.auth = None
        self.tls = None

    def publish_multiple(self, msgs):
        return paho.mqtt.publish.multiple(msgs, hostname=self.hostname, port=self.port, client_id=self.client_id)
