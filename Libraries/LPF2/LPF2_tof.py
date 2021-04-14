import gc,utime
import micropython
import LPF2_esp as LPF2
from machine import I2C,Pin
from vl53 import *

micropython.alloc_emergency_exception_buf(200)

modes = [
LPF2.mode('int8',type = LPF2.DATA8),
LPF2.mode('int16', type = LPF2.DATA16),
LPF2.mode('int32', type = LPF2.DATA32),
LPF2.mode('float', format = '2.1', type = LPF2.DATAF),
LPF2.mode('int8_array',size = 4, type = LPF2.DATA8),
LPF2.mode('int16_array',size = 4, type = LPF2.DATA16),
LPF2.mode('int32_array',size = 4, type = LPF2.DATA32),
LPF2.mode('float_array',size = 4, format = '2.1', type = LPF2.DATAF)
]

# Name, Format [# datasets, type, figures, decimals], 
# raw [min,max], Percent [min,max], SI [min,max], Symbol, functionMap [type, ?], view
mode0 = ['LPF2-DETECT',[1,LPF2.DATA8,3,0],[0,255],[0,100],[0,255],'',[LPF2.ABSOLUTE,0],True]
mode1 = ['LPF2-COUNT',[1,LPF2.DATA32,4,0],[0,100],[0,100],[0,100],'CNT',[LPF2.ABSOLUTE,0],True]
mode2 = ['LPF2-CAL',[3,LPF2.DATAF,3,0],[0,1023],[0,100],[0,1023],'RAW',[LPF2.ABSOLUTE,LPF2.ABSOLUTE],False]
modes2 = [mode0,mode1,mode2]     

led = Pin(2, mode=Pin.OUT)
led.on()
txpin=1
rxpin=3
lpf2 = LPF2.ESP_LPF2(0, txpin,rxpin, modes2, LPF2.SPIKE_Ultrasonic, timer = -1, freq = 5)    # ESP
#lpf2 = LPF2.Prime_LPF2(1, 'Y1', 'Y2', modes, LPF2.SPIKE_Ultrasonic, timer = 4, freq = 5)    # PyBoard
# use EV3_LPF2 or Prime_LPF2 - also make sure to select the port type on the EV3 to be ev3-uart


i2c=I2C(scl=Pin(5),sda=Pin(4))
tof=VL53L0X(i2c)    
tof.start()

lpf2.initialize()

value = 0

# Loop
while True:
     if not lpf2.connected:
          lpf2.sendTimer.deinit()
          led.on()
          utime.sleep_ms(200)
          lpf2.initialize()
     else:
          led.off()
          val1=tof.read()/10.
          print(val1)
          print("type val",type(val1))
          value=int(val1)
          print("type value",type(value))
          #mode=lpf2.current_mode
          lpf2.load_payload('uInt8',value)
          print(value)
          utime.sleep_ms(20)
          