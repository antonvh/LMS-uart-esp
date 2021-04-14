from lpf2 import *

lpf2 = LPF2()

lpf2.initialize()

value = 0
while True:
  if not lpf2.connected:
    print('not connected')
    utime.sleep(1)
    lpf2.initialize()
  else:
    if value<9:
      value=value+1
    else: 
      value=0
    lpf2.send_value(value)
    utime.sleep_ms(200)