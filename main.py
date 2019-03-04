import time
from machine import Pin
from machine import PWM
from umqtt.robust import MQTTClient

from credentials import MQTT_SERVER
from credentials import MQTT_USERNAME
from credentials import MQTT_PASSWORD

CLIENT_ID = "cat_feeder_test"

TOPIC = CLIENT_ID + "/feed"
STATUS_TOPIC = CLIENT_ID + "/status"
LAST_FED_TOPIC = CLIENT_ID + "/last_fed"
DONE_TOPIC = CLIENT_ID + "/done_feeding"


class CatFeeder(object):
    def __init__(self):
        """"""
        self._client = None
        self._button = Pin(14, mode=Pin.IN, pull=Pin.PULL_UP)

        self._servo_buzz = Feeder(
                        pin_servo=12,
                        # pin_distance_sensor=XXX,
                        open_gate=47,
                        pause=0.35,
                        )

        self._servo_tuxedo = Feeder(
                        pin_servo=5,
                        # pin_distance_sensor=XXX,
                        open_gate=45,
                        pause=0.365,
                        )

        print('Instancing button and servos.')

        self._button.irq(
          handler=self.button_pressed,
          trigger=Pin.IRQ_RISING
        )

        print('Setting IRQ.')

        self._done_payload = 'Done feeding!'

        self.mqtt_connect()

    def mqtt_connect(self):
        """"""
        print("Connecting to MQTT server...")

        self._client = MQTTClient(
            CLIENT_ID,
            MQTT_SERVER,
            user=MQTT_USERNAME,
            password=MQTT_PASSWORD
          )

        self._client.set_callback(self.on_message)

        print("Connecting MQTT")

        self._client.set_last_will(
            STATUS_TOPIC,
            "Offline",
            retain=True
          )

        self._client.connect()

        self._client.subscribe(TOPIC)

        print("Connected to %s, subscribed to %s topic" % (
                MQTT_SERVER,
                TOPIC
            )
        )

        self._client.publish(STATUS_TOPIC, "Connected", retain=True)

        try:
            while True:
                self._client.wait_msg()
        finally:
            self._client.disconnect()

    def button_pressed(self, pin):
        if pin.value() == 1:
            self._servo_tuxedo.feed()
            self._servo_buzz.feed()
            self.done_feeding()

    def on_message(self, topic, message):
        """"""
        print(topic, message)

        msg = message.strip().decode('utf-8')

        if msg == "feed":
            self._client.publish(LAST_FED_TOPIC, "Feeding...")

            try:
                self._servo_tuxedo.feed()
                self._servo_buzz.feed()
            except:
                self._done_payload = 'Error. Bad message format. Payload was: %s' % msg

        self.done_feeding()

    def done_feeding(self):
        """"""
        self._client.publish(
          DONE_TOPIC,
          self._done_payload
        )

        print("Done feeding!")


class Feeder(object):
    def __init__(
        self,
        pin_servo=None,
        pin_distance_sensor=None,
        open_gate=47,
        pause=0.3,
    ):

        self._open_position = open_gate
        self._pause_open = pause
        self._close_position = 75

        self._servo = PWM(Pin(pin_servo), freq=50, duty=self._close_position)

        if pin_distance_sensor:
            self._distance_sensor = Pin(pin_distance_sensor, Pin.IN)

    @staticmethod
    def get_remaining_food():
        multiplier = 1
        return multiplier

    def feed(self):
        """"""
        multiplier = self.get_remaining_food()
        self._servo.duty(self._open_position * multiplier)
        time.sleep(self._pause_open)
        self._servo.duty(self._close_position)


if __name__ == "__main__":
    cf = CatFeeder()
