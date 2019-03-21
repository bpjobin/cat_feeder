import time
from machine import Pin
from machine import PWM
from umqtt.robust import MQTTClient

from credentials import MQTT_SERVER
from credentials import MQTT_USERNAME
from credentials import MQTT_PASSWORD

CLIENT_ID = "cat_feeder"

TOPIC = CLIENT_ID + "/feed"
STATUS_TOPIC = CLIENT_ID + "/status"
LAST_FED_TOPIC = CLIENT_ID + "/last_fed"
DONE_TOPIC = CLIENT_ID + "/done_feeding"
QTY_BUZZ_TOPIC = CLIENT_ID + "/buzz_quantity"
QTY_TUXEDO_TOPIC = CLIENT_ID + "/tuxedo_quantity"
MANUAL_FEEDING = CLIENT_ID + "/manual_feeding"


class CatFeeder(object):
    def __init__(self):
        """"""
        self._client = None
        self._button = Pin(14, mode=Pin.IN, pull=Pin.PULL_UP)
        self._done_payload = 'Done feeding!'

        self._servo_buzz = Feeder(
            pin_servo=12,
            trigger=2,
            echo=0,
        )

        self._servo_tuxedo = Feeder(
            pin_servo=5,
            trigger=13,
            echo=15,
        )

        print('Instancing button and servos.')
        self._button.irq(
            handler=self.button_pressed,
            trigger=Pin.IRQ_RISING
        )
        print('Setting IRQ.')

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

        while True:
            self._client.wait_msg()

    def button_pressed(self, pin):
        if pin.value():
            time.sleep_ms(300)
            print('#' * 80)
            self._client.publish(MANUAL_FEEDING, "")
            self._client.wait_msg()

    def set_open_infos(self, infos):
        """"""
        self._servo_buzz.open_position = infos.get("open_buzz")
        self._servo_tuxedo.open_position = infos.get("open_tuxedo")
        self._servo_buzz.pause_open = infos.get("pause_buzz")
        self._servo_tuxedo.pause_open = infos.get("pause_tuxedo")

    def on_message(self, topic, message):
        """"""
        print(topic, message)

        msg = message.strip().decode('utf-8')

        self.set_open_infos(eval(msg))

        try:
            self._client.publish(LAST_FED_TOPIC, "Feeding...")
            self._servo_tuxedo.feed()
            time.sleep(1)
            self._servo_buzz.feed()
        except:
            self._done_payload = 'Error. Bad message format. Payload was: %s' % msg

        self.done_feeding()

    def done_feeding(self):
        """"""
        time.sleep(0.2)
        self._client.publish(
            DONE_TOPIC,
            self._done_payload
        )
        time.sleep(0.2)
        self._client.publish(
            QTY_BUZZ_TOPIC,
            self._servo_buzz.remaining_quantity
        )
        time.sleep(0.2)
        self._client.publish(
            QTY_TUXEDO_TOPIC,
            self._servo_tuxedo.remaining_quantity
        )

        print("Done feeding!\n\n")
        print('/' * 80)
        print('Waiting for message...')
        self._client.wait_msg()


class Feeder(object):
    def __init__(
            self,
            pin_servo=None,
            trigger=None,
            echo=None,
    ):

        self._open_position = None
        self._open_position_max = 38
        self._pause_open = None
        self._pause_open_max = 0.8
        self._close_position = 77
        self._trigger = trigger
        self._remaining_quantity = None
        self._full_quantity = 1
        self._empty_quantity = 25
        self._distance_cm = None

        self._servo = PWM(Pin(pin_servo), freq=50, duty=self._close_position)

        if self._trigger:
            self._distance_trigger = Pin(trigger, Pin.OUT)
            self._distance_echo = Pin(echo, Pin.IN)

    @property
    def open_position(self):
        return float(self._open_position)

    @open_position.setter
    def open_position(self, value):
        self._open_position = float(value)

    @property
    def pause_open(self):
        return float(self._pause_open)

    @pause_open.setter
    def pause_open(self, value):
        self._pause_open = float(value)

    @property
    def remaining_quantity(self):
        """"""
        if not self._trigger:
            return str(-1)

        if self._distance_cm is None:
            return str(-1)

        result = self.map_range(
            self.distance_cm,
            (self._empty_quantity, self._full_quantity),
            (0, 100)
        )

        print('Full at %s%s.' % (result, "%"))
        return str(result)

    @remaining_quantity.setter
    def remaining_quantity(self, value):
        self._remaining_quantity = value

    @property
    def distance_cm(self):
        return self._distance_cm

    @distance_cm.setter
    def distance_cm(self, value):
        self._distance_cm = value

    def distance_in_cm(self):
        start = 0
        end = 0

        self._distance_trigger.on()
        time.sleep_us(10)
        self._distance_trigger.off()

        while self._distance_echo.value() == 0:
            start = time.ticks_us()

        while self._distance_echo.value() == 1:
            end = time.ticks_us()

        diff = time.ticks_diff(start, end)

        # Calc the duration of the recieved pulse, divide the result by
        # 2 (round-trip) and divide it by 29 (the speed of sound is
        # 340 m/s and that is 29 us/cm).
        dist_in_cm = (diff / 2) / 29

        self._distance_cm = -dist_in_cm
        print("Distance: %s cm." % self._distance_cm)
        if self._distance_cm > self._empty_quantity:
            self._distance_cm = self._empty_quantity
        return self._distance_cm

    def get_opening_ratio(self):
        """"""
        if not self._trigger:
            return self._open_position, self._pause_open

        dist = self.distance_in_cm()

        opening_ratio = self.map_range(
            dist,
            (self._empty_quantity, self._full_quantity),
            (self._open_position_max, self._open_position)
        )
        pause_ratio = self.map_range(
            dist,
            (self._empty_quantity, self._full_quantity),
            (self._pause_open, self._pause_open_max)
        )

        if pause_ratio > 2:
            pause_ratio = 2

        return opening_ratio, pause_ratio

    @staticmethod
    def map_range(value, old_range, new_range):
        """"""
        old_range_max, old_range_min = old_range
        old_range = old_range[0] - old_range[1]
        new_range_max, new_range_min = new_range
        new_range = new_range[0] - new_range[1]

        new_value = ((value - old_range_min) * new_range / old_range) + new_range_min

        return round(new_value, 2)

    def feed(self):
        """"""
        open_ratio, pause_ratio = self.get_opening_ratio()
        print('Opening to: %i degrees.' % open_ratio)
        print('Pausing for: %f sec.\n' % pause_ratio)

        self._servo.duty(int(round(open_ratio, 0)))
        time.sleep(pause_ratio)
        self._servo.duty(self._close_position)

        return


if __name__ == "__main__":
    cf = CatFeeder()

