import time
from machine import Pin
from machine import PWM

CLOSED_POSITION = 75

button = Pin(14, Pin.IN, Pin.PULL_UP)

servo_buzz = PWM(
	Pin(12),
	freq=50,
	duty=CLOSED_POSITION
	)

servo_tuxedo = PWM(
	Pin(5),
	freq=50,
	duty=CLOSED_POSITION
	)

def open_and_close():
	""""""
	servo_buzz.duty(47) # petite croquette --> 47
	time.sleep(0.35) # petite croquette --> 0.21
	servo_buzz.duty(CLOSED_POSITION)

	time.sleep(1)

	servo_tuxedo.duty(45)
	time.sleep(0.365)
	servo_tuxedo.duty(CLOSED_POSITION)


def go():
	while True:
		if button.value() == 1:
			print(button.value())
			open_and_close()


go()