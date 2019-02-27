import time
from machine import Pin
from machine import PWM
from rtttl import RTTTL
import songs

piezo_pin = PWM(Pin(5))
volume = 20

def play_tone(freq, msec):
	""""""
	print('freq = {:6.1f} msec = {:6.1f}'.format(freq, msec))
	if freq > 0:
		piezo_pin.freq(int(freq))
		piezo_pin.duty(volume)
	time.sleep_ms(int(msec * 0.9))
	piezo_pin.duty(0)
	time.sleep_ms(int(msec * 0.1))


def play_song(s, duration):
	""""""
	note = 0
	tune = RTTTL(songs.find(s))
	for freq, msec in tune.notes():
		if note < duration:
			play_tone(freq, msec)
		note += 1