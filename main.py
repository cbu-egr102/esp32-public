import machine;
import network;
import sensors
import gc;

def start():
  def print_f(msg):
    with open("log.txt", "a") as file:
      file.write(msg.strip() + "\n")
    gc.collect()

  print_f("===========================\nline 138: Start")
  # process config
  bot_id = -1
  wifi_name = ""
  wifi_pswd = ""
  aws_endpoint = ""
  dist_sensors = {}
  i2c_pins = {}
  adcs = []

  # print_f("line 148: processing config")
  with open("config.txt") as config_file:
    for line in config_file.read().splitlines():
      args = line.split()
      if not args:
        continue
      if args[0] == "id":
        bot_id = int(args[1])
      elif args[0] == "wifi":
        wifi_name = " ".join(args[1:])
      elif args[0] == "w_pwd":
        wifi_pswd = " ".join(args[1:])
      elif args[0] == "aws_endp":
        aws_endpoint = args[1]
      elif args[0] in ["scl", "sda"]:
        i2c_pins[args[0]] = int(args[1])
      elif args[0][0] == "d":
        dist_sensors[args[0]] = [int(n) for n in args[1:]]
      elif args[0].startswith("adc"):
        adcs.append((args[1], int(args[2], 16)))
  gc.collect()
  # print_f("line 169: config processed")

  # set up wifi
  machine.freq(160 * 10 ** 6)
  # print_f("line 173: connecting to wifi")
  wlan = network.WLAN(network.STA_IF)
  gc.collect()
  # print_f("line 175: started wlan")
  wlan.active(True)
  gc.collect()
  # print_f("line 177: set wlan to active")
  wlan.connect(wifi_name, wifi_pswd)
  # print_f("line 179: connected to network")
  gc.collect()

  while not wlan.isconnected():
    machine.idle()

  # print_f("Line 180: pre-loop")
  # machine.freq(240 * 10 ** 6)
  try:
    import urequests
    gc.collect()
    ads = sensors.AnalogReader(i2c_pins["sda"], i2c_pins["scl"], adcs[0][1], adcs[1][1], adcs[0][0] + adcs[1][0])
    distance_sensors = [sensors.HCSR04(t, e) for t, e in dist_sensors.values()]
    ctr = 0
    # print_f("Line 185: sensors instantiated")
    while True:
      gc.collect()
      data = [bot_id] + [ds.distance_mm() for ds in distance_sensors[:2]]\
           + ads.read_sensor_values("vvlle")
      data_str = str(data).replace(" ", "")
      gc.collect()
      try:
        response = urequests.get(aws_endpoint+"?data="+data_str, timeout=10)
        print(aws_endpoint+"?data="+data_str)
        print(ctr, ": Posted:", data_str)
        # print_f("line 197: posted data")
        ctr += 1
        body = response.json()
        print("Response:", body)
        # print_f("Response: " + str(body))
        if body["endLoop"]:
          print("Server issued Kill Signal. Stopping!")
          break
      except (IndexError, KeyError, OSError) as e:
        print("An error was produced: ", e)
        # print_f("Error produced!")
        if not wlan.isconnected():
          print("The WiFi disconnected. Reconnecting...")
          wlan.active(True)
          wlan.connect(wifi_name, wifi_pswd)
          while not wlan.isconnected():
            machine.idle()
  finally:
    if wlan and wlan.isconnected():
      wlan.disconnect()
      wlan.active(False)

start()