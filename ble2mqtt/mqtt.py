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

        self.status_topic = 'ble2mqtt'

        self.mqtt_client = paho.mqtt.client.Client()
        self.mqtt_client.max_inflight_messages_set(5)
        self.mqtt_client.max_queued_messages_set(5)

        self.mqtt_client.will_set(self.status_topic, 'OFF', 0, True)

        self.mqtt_client.on_connect=self.on_connect
        self.mqtt_client.on_disconnect=self.on_disconnect

        self.connected = False
        self._connect()

        self.mqtt_client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to MQTT")
        self.connected = True
        self.mqtt_client.publish(self.status_topic, 'ON', 0, False)

    def on_disconnect(self, client, userdata,  rc):
        print("Disconnected from MQTT")
        self.connected = False

    def _connect(self):
        if self.connected:
            return True

        try:
            self.mqtt_client.connect(self.hostname, self.port, 10)
            return True
        except ConnectionError as e:
            print("Could not connect to MQTT: {} - will keep trying".format(e))

        return False

    def publish_multiple(self, msgs):
        """ This makes its own connection, publishes and disconnects - in additionl to our other """
        """ connection which just provides status """
        self._connect()
        return paho.mqtt.publish.multiple(msgs, hostname=self.hostname, port=self.port, client_id=self.client_id)

    def __del__(self):
        if self.connected:
            self.mqtt_client.publish(self.status_topic, 'OFF', 0, False)

