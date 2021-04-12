import hub,utime

hub.port.A.info()


while True:
  try:
    value = hub.port.A.device.get()[0]
    print(value)
    hub.display.show(str(value))
    utime.sleep(0.2)
  except:
    utime.sleep(0.2)
    print("not connected")