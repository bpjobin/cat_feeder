import time
import ubinascii
from machine import Pin
from machine import PWM
from machine import unique_id
from umqtt.robust import MQTTClient

from credentials import MQTT_SERVER
from credentials import MQTT_USERNAME
from credentials import MQTT_PASSWORD

TOPIC = "cat_feeder_test/feed"
STATUS_TOPIC = "cat_feeder_test/status"
LAST_FED_TOPIC = "cat/last_fed"
DONE_TOPIC = "cat_feeder/done_feeding"

CLIENT_ID = "cat_feeder_test"

CLOSED_POSITION = 75

button = Pin(14, Pin.IN, Pin.PULL_UP)

servo_buzz = PWM(
	Pin(12),
	freq=50,
	duty=CLOSED_POSITION
	)
# time.sleep(0.5)
servo_tuxedo = PWM(
	Pin(5),
	freq=50,
	duty=CLOSED_POSITION
	)

# servo_buzz.duty(CLOSED_POSITION)
# time.sleep(0.5)
# servo_tuxedo.duty(CLOSED_POSITION)


def mqtt_connect():
	""""""
	print("Connecting to MQTT server...")

	global client
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
			if button.value() == 1:
				open_and_close()

	finally:
		client.disconnect()


def on_message(topic, message):
	""""""
	print(topic, message)

	msg = message.strip().decode('utf-8')

	if msg == "feed":
		client.publish(LAST_FED_TOPIC, "Feeding...")
		done_payload = 'Done feeding!'

		try:
			open_and_close()
		except:
			done_payload = 'Error. Bad message format. Payload was: %s' % msg
		
def done_feeding():
	""""""
	client.publish(
	DONE_TOPIC,
	done_payload
	)
	
	print("Done feeding!")


def open_and_close():
	""""""
	servo_buzz.duty(47) # petite croquette --> 47
	time.sleep(0.35) # petite croquette --> 0.21
	servo_buzz.duty(CLOSED_POSITION)

	time.sleep(1)

	servo_tuxedo.duty(45)
	time.sleep(0.365)
	servo_tuxedo.duty(CLOSED_POSITION)

	done_feeding()

mqtt_connect()