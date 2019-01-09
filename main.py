import time
import ubinascii
from machine import Pin
from machine import PWM
from machine import unique_id
from umqtt.robust import MQTTClient

from credentials import MQTT_SERVER
from credentials import MQTT_USERNAME
from credentials import MQTT_PASSWORD

TOPIC = "cat_feeder/feed"
CLIENT_ID = ubinascii.hexlify(unique_id())

global closed_position
closed_position = 75

servo_buzz = PWM(
	Pin(14),
	freq=50,
	duty=closed_position
	)
time.sleep(0.5)
servo_tuxedo = PWM(
	Pin(12),
	freq=50,
	duty=closed_position
	)

servo_buzz.duty(closed_position)
time.sleep(0.5)
servo_tuxedo.duty(closed_position)


def mqtt_connect():
	print("Connecting to MQTT server...")

	global client
	client = MQTTClient(
		CLIENT_ID,
		MQTT_SERVER,
		user=MQTT_USERNAME,
		password=MQTT_PASSWORD
		)

	client.set_callback(on_message)
	print("Connecting MQTT as clean session")
	client.set_last_will("cat_feeder/status", "Offline")
	client.connect(clean_session=True)
	client.subscribe(TOPIC)
	print("Connected to %s, subscribed to %s topic" % (
		MQTT_SERVER,
		TOPIC
		)
	)
	client.publish("cat_feeder/status", "Connected")

	try:
		while 1:
			client.publish("cat_feeder/status", "Ready")
			client.wait_msg()

	finally:
		client.disconnect()


def on_message(topic, message):
	""""""
	print(topic, message)

	msg = message.strip().decode('utf-8')

	if msg == "feed":
	 	client.publish("cat/last_fed", "Feeding...")
	 	done_payload = 'Done feeding!'

	 	try:
			open_and_close()
		except:
			done_payload = 'Error. Bad message format. Payload was: %s' % msg
		

		client.publish(
		"cat_feeder/done_feeding",
		done_payload
		)
		
		print("Done feeding!")


def open_and_close():
	""""""
	servo_buzz.duty(47)
	time.sleep(0.21)
	servo_buzz.duty(closed_position)

	servo_tuxedo.duty(45)
	time.sleep(0.365)
	servo_tuxedo.duty(closed_position)


mqtt_connect()