import time
from machine import Pin
from machine import PWM
from machine import enable_irq
from machine import disable_irq


class CatFeeder(object):
    def __init__(self):
        """"""
        print('Instancing button.')
        self._button = Pin(5, mode=Pin.IN, pull=Pin.PULL_UP)

        print('Setting IRQ.')
        self._button.irq(
            handler=self.button_pressed,
            trigger=Pin.IRQ_RISING
        )

    def button_pressed(self, pin):
        previous_state = disable_irq()
        self._initialize_servos()

        if pin.value():
            time.sleep_ms(300)
            self.feed()
            print('#' * 80)

        self._deinit_servos()
        enable_irq(previous_state)

    def _initialize_servos(self):
        """"""
        print('Instancing servos.')
        self._servo_buzz = Feeder(
            pin_servo=0,
        )

        self._servo_tuxedo = Feeder(
            pin_servo=4,
        )
        time.sleep_ms(500)

    def _deinit_servos(self):
        """"""
        print('Deinit servos.')
        self._servo_buzz.deinit_servo()
        self._servo_tuxedo.deinit_servo()

    def feed(self):
        """"""
        time.sleep(0.2)
        self._servo_buzz.feed()
        print('fed buzz')
        time.sleep(1)
        print('pause 1 sec')
        self._servo_tuxedo.feed()
        print('fed tuxedo')

        print("Done feeding!\n\n")
        print('/' * 80)
        print('Waiting for message...')

    def open_close_test(self, open_=48, pause=1):
        """"""
        self._servo_buzz.open_position = open_
        self._servo_tuxedo.open_position = open_
        self._servo_buzz.pause_open = pause
        self._servo_tuxedo.pause_open = pause

        self._servo_buzz.feed()
        print('fed buzz')
        time.sleep(1)
        print('pause 1 sec')
        self._servo_tuxedo.feed()


class Feeder(object):
    def __init__(
            self,
            pin_servo=None,
    ):
        """
        servo's minimum duty 27
        """
        self._open_position = 42
        self._pause_open = 1
        self._close_position = 77

        self._servo = PWM(
            Pin(pin_servo, Pin.OUT),
            freq=50,
            duty=self._close_position
        )

    def deinit_servo(self):
        """"""
        self._servo.deinit()

    def feed(self):
        """"""
        print('Opening to: %i degrees.' % self._open_position)
        print('Pausing for: %f sec.\n' % self._pause_open)

        self._servo.duty(int(round(self._open_position)))
        time.sleep(self._pause_open)
        self._servo.duty(self._close_position)
