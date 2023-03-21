import machine
import network

wifi_name = ""
wifi_pswd = ""

def read_config():
    with open("config.txt") as config_file:
        for line in config_file.read().splitlines():
            args = line.split()
            if not args:
                continue
            elif args[0] == "wifi":
                wifi_name = " ".join(args[1:])
            elif args[0] == "w_pwd":
                wifi_pswd = " ".join(args[1:])

def wifi_setup():
    # set up wifi
    read_config()
    machine.freq(160 * 10 ** 6)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(wifi_name, wifi_pswd)

    while not wlan.isconnected():
        machine.idle()

def wifi_disconnect():
    wlan = network.WLAN(network.STA_IF)
    if wlan and wlan.isconnected():
        wlan.disconnect()
        wlan.active(False)

def wifi_reconnect():
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print("The WiFi disconnected. Reconnecting...")
        wlan.active(True)
        wlan.connect(wifi_name, wifi_pswd)
        while not wlan.isconnected():
            machine.idle()