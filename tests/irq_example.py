from machine import Pin
import esp
from machine import Timer
import time

esp.osdebug(None)


# def handle_tip(p):
#     print('tip')
#     bucket = Pin(0, Pin.IN, Pin.PULL_UP)
#     bucket_irq = bucket.irq(trigger=Pin.IRQ_RISING, handler=handle_tip)
#     bucket_irq
#
#     bucket_irq.disable()
#
#
# def handle_tip(p):
#     self.state = machine.disable_irq()
#     print('tip')
#     tim = Timer(-1)
#     tim.init(period=DEBOUNCE_TIME, mode=Timer.ONE_SHOT, callback=lambda t:machine.enable_irq(self.state))


def check_switch(p):
    global switch_state
    global switched
    global last_switch_state
    switch_state = switch.value()
    if switch_state != last_switch_state:
        switched = True
    last_switch_state = switch_state


switch = Pin(0, Pin.IN, Pin.PULL_UP)
switch_state = switch.value()
last_switch_state = switch_state
switched = False

tim = Timer(-1)
tim.init(period=50, mode=Timer.PERIODIC, callback=check_switch)

while True:
  if switched:
    if switch_state == 1:
      print('tipped')
    switched = False
  time.sleep_ms(20)