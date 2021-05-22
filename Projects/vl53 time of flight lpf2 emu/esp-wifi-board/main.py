from utime import sleep_ms
import LPF2_esp as LPF2
from machine import I2C,Pin
from vl53 import *
from uos import dupterm

dupterm(None, 1)

# Name, Format [# datasets, type, figures, decimals], 
# raw [min,max], Percent [min,max], SI [min,max], Symbol, functionMap [type, ?], view
mode0 = ['DISTANCE',[1,LPF2.DATA16,3,0],[0,900],[0,100],[0,900],'cm',[LPF2.ABSOLUTE,0],True]
modes=[mode0]   

led = Pin(2, mode=Pin.OUT)
led.on()
txpin=1
rxpin=3
lpf2 = LPF2.ESP_LPF2(0, txpin,rxpin, modes, LPF2.SPIKE_Ultrasonic, timer = -1, freq = 5)    # ESP


i2c=I2C(scl=Pin(5),sda=Pin(4))
tof=VL53L0X(i2c)    
tof.start()

lpf2.initialize()

value = 0

# Loop
while True:
     try:
          if not lpf2.connected:
               lpf2.sendTimer.deinit()
               led.on()
               sleep_ms(200)
               lpf2.initialize()
          else:
               led.off()
               val1=tof.read()/10. # mm to cm
               value=int(val1-4) # offset on my sensor is 4 cm
               lpf2.load_payload('Int16',value)
               sleep_ms(20)
     except:
          lpf2.close() # clean up
          raise
          