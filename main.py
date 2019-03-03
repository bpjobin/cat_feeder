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
  def __init__(*args, **kwargs):
    self._button = Pin(id=14, mode=Pin.IN, pull=Pin.PULL_UP)
    
    self._servo_buzz = Feeder(
                    pin_servo=12,
                    pin_distance_sensor=XXX,
                    open=47,
                    pause=0.35,
                    )
    self._servo_tuxedo = Feeder(
                    pin_servo=5,
                    pin_distance_sensor=XXX,
                    open=45,
                    pause=0.365,
                    )
    
    self._button.irq(
      handler=self.button_pressed,
      trigger=Pin.IRQ_RISING
    )
    
    self.mqtt_connect()
    
  def mqtt_connect():
    """"""
    print("Connecting to MQTT server...")

    client = MQTTClient(
      CLIENT_ID,
      MQTT_SERVER,
      user=MQTT_USERNAME,
      password=MQTT_PASSWORD
      )

    client.set_callback(on_message)
    print("Connecting MQTT")
    client.set_last_will(
      STATUS_TOPIC,
      "Offline",
      retain=True
      )

    client.connect()
    client.subscribe(TOPIC)
    print("Connected to %s, subscribed to %s topic" % (
      MQTT_SERVER,
      TOPIC
      )
    )
    client.publish(STATUS_TOPIC, "Connected", retain=True)

    try:
      while True:
        client.wait_msg()

    finally:
      client.disconnect()

  def button_pressed(self, pin):
    if pin.value() == 1:
      self._servo_tuxedo.feed()
      self._servo_buzz.feed()
      self.done_feeding()
  
  def on_message(topic, message):
    """"""
    print(topic, message)

    msg = message.strip().decode('utf-8')

    if msg == "feed":
      client.publish(LAST_FED_TOPIC, "Feeding...")
      done_payload = 'Done feeding!'

      try:
        self._servo_tuxedo.feed()
        self._servo_buzz.feed()
        self.done_feeding()
      except:
        done_payload = 'Error. Bad message format. Payload was: %s' % msg

  
  def done_feeding():
    """"""
    client.publish(
    DONE_TOPIC,
    done_payload
    )

    print("Done feeding!")


class Feeder(object):
  def __init__(
    self,
    pin_servo=None,
    pin_distance_sensor,
    open=47,
    pause=0.3,
    *args,
    **kwargs
    ):
    
    self._open_position = open
    self._pause_open = pause
    self._close_position = 75
    
    self._servo = PWM(Pin(pin_servo), freq=50, duty=self._close_position)
    self._distance_sensor = Pin(pin_distance_sensor, Pin.IN)
  
  def get_remaining_food(self):
    multiplier = 1
    return multiplier
  
  def feed():
    """"""
    multiplier = self.get_remaining_food()
    self.servo.duty(self._open_position * multiplier)
    time.sleep(self._pause_open)
    self.servo.duty(self._close_position)


if __name__ == "__main__":
  cf = CatFeeder()
