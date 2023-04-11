import sensors
import wifi
import urequests

def start():
  # process config
  bot_id = -1
  aws_endpoint = ""
  dist_sensors = {}
  i2c_pins = {}
  adcs = []

  # print_f("line 148: processing config")
  with open("bot.config") as config:
    for line in config.read().splitlines():
      args = line.split()
      if not args:
        continue
      if args[0] == "id":
        bot_id = int(args[1])

  with open("general.config") as config:
    for line in config.read().splitlines():
      args = line.split()
      if not args:
        continue
      if args[0] == "aws_endp":
        aws_endpoint = args[1]
      elif args[0] in ["scl", "sda"]:
        i2c_pins[args[0]] = int(args[1])
      elif args[0][0] == "d":
        dist_sensors[args[0]] = [int(n) for n in args[1:]]
      elif args[0].startswith("adc"):
        adcs.append((args[1], int(args[2], 16)))
  # print_f("line 169: config processed")

  # print_f("Line 180: pre-loop")
  try:
    ads = sensors.AnalogReader(i2c_pins["sda"], i2c_pins["scl"], adcs[0][1], adcs[1][1], adcs[0][0] + adcs[1][0])
    distance_sensors = [sensors.HCSR04(t, e) for t, e in dist_sensors.values()]
    # print_f("Line 185: sensors instantiated")
    while True:
      data = [bot_id] + [ds.distance_mm() for ds in distance_sensors[:2]] + ads.read_sensor_values("vvlle")
      data_str = str(data).replace(" ", "")
      try:
        response = urequests.get(aws_endpoint+"?data="+data_str)
        print(aws_endpoint+"?data="+data_str)
        body = response.json()
        print("Response:", body)
        if body["endLoop"]:
          print("Server issued Kill Signal. Stopping!")
          break
      except (IndexError, KeyError, OSError) as e:
        print("An error was produced: ", e)
        # print_f("Error produced!")
  finally:
    wifi.wifi_disconnect()

start()
