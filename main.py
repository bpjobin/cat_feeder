import time
import ubinascii
from machine import Pin
from machine import PWM
from machine import unique_id
from umqtt.robust import MQTTClient
from rtttl import RTTTL
import songs

from credentials import MQTT_SERVER
from credentials import MQTT_USERNAME
from credentials import MQTT_PASSWORD

TOPIC = "cat_feeder/feed"
CLIENT_ID = ubinascii.hexlify(unique_id())

global closed_position
closed_position = 75

piezo_pin = PWM(Pin(5))

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
	print("Connecting MQTT as clean session")
	client.set_last_will("cat_feeder/status", "Offline")
	client.connect()
	client.subscribe(TOPIC)
	print("Connected to %s, subscribed to %s topic" % (
		MQTT_SERVER,
		TOPIC
		)
	)
	client.publish("cat_feeder/status", "Connected", retain=True)
	client.publish("cat_feeder/status", "Ready", retain=True)

	try:
		while 1:
			client.wait_msg()

	finally:
		client.disconnect()


def on_message(topic, message, song):
	""""""
	print(topic, message)

	msg = message.strip().decode('utf-8')

	if msg == "feed":
		play_song(song)
		time.sleep(1)
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


def play_tone(freq, msec):
	""""""
    print('freq = {:6.1f} msec = {:6.1f}'.format(freq, msec))
    if freq > 0:
        buz_tim.freq(int(freq))
        buz_tim.duty(50)
    time.sleep_ms(int(msec * 0.9))
    buz_tim.duty(0)
    time.sleep_ms(int(msec * 0.1))


def play_song(s):
	""""""
    tune = RTTTL(songs.find(s))
    for freq, msec in tune.notes():
        play_tone(freq, msec)

mqtt_connect()