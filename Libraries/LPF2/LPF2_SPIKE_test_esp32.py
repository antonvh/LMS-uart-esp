import hub,utime

hub.port.B.info()


cnt=0
mode=0
hub.port.B.device.mode(mode)
while True:
  cnt+=1
  if cnt>30:
      mode=(mode+1)%3
      cnt=0
      print("switch to mode",mode)
      try:
          hub.port.B.device.mode(mode)
      except:
          print("error setting mode")
  try:
    value = hub.port.B.device.get()[0]
    print(value)
    if mode==0:
        hub.display.show(str(value))
    elif mode==2: # float
        print(struct.unpack('>f',struct.pack('i',value))[0])
    utime.sleep(0.2)
  except:
    utime.sleep(0.2)
    print("not connected")