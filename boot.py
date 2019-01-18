import gc
from credentials import SSID
from credentials import SSID_PASSWORD
from credentials import STATIC_IP

gc.collect()

def connect():
	import network

	sta_if = network.WLAN(network.STA_IF)
	if not sta_if.isconnected():
		print ('connecting to network...')
		sta_if.active(True)
		if STATIC_IP:
			sta_if.config(
				STATIC_IP,
				"255.255.255.0",
				"192.168.1.1",
				"8.8.8.8"
				)
			
		sta_if.connect(SSID, SSID_PASSWORD)
		while not sta_if.isconnected():
			pass
	print("network config: ", sta_if.ifconfig())


def no_debug():
	import esp
	esp.osdebug(None)

# no_debug()
connect()
