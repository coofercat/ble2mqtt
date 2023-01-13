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
        self.status_online = False

        self.mqtt_client = paho.mqtt.client.Client()
        self.mqtt_client.max_inflight_messages_set(5)
        self.mqtt_client.max_queued_messages_set(5)

        self.mqtt_client.on_connect=self.on_connect
        self.mqtt_client.on_disconnect=self.on_disconnect

        self.connected = False
        self._connect()

        self.mqtt_client.loop_start()

    def publish_online(self):
        if self.connected:
            self.mqtt_client.publish(self.status_topic, 'ON', 0, False)
        self.status_online = True

    def publish_offline(self):
        if self.connected:
            self.mqtt_client.will_set(self.status_topic, 'OFF', 0, True)
        self.status_online = False

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to MQTT")
        self.connected = True
        self.publish_online()

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
        out = paho.mqtt.publish.multiple(msgs, hostname=self.hostname, port=self.port, client_id=self.client_id)
        if out:
            if self.status_online == False:
                self.publish_online()
        else:
            self.publish_offline()
        return out

    def __del__(self):
        self.publish_offline()

