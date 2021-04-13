import gc,utime
import micropython
import LPF2_esp as LPF2
from machine import Pin
micropython.alloc_emergency_exception_buf(200)

modes = [
LPF2.mode('int8',type = LPF2.DATA8),
# LPF2.mode('int16', type = LPF2.DATA16),
# LPF2.mode('int32', type = LPF2.DATA32),
# LPF2.mode('float', format = '2.1', type = LPF2.DATAF),
# LPF2.mode('int8_array',size = 4, type = LPF2.DATA8),
# LPF2.mode('int16_array',size = 4, type = LPF2.DATA16),
# LPF2.mode('int32_array',size = 4, type = LPF2.DATA32),
# LPF2.mode('float_array',size = 4, format = '2.1', type = LPF2.DATAF)
]

led = Pin(2, mode=Pin.OUT)
led.on()
txpin=1
rxpin=3
lpf2 = LPF2.ESP_LPF2(0, txpin,rxpin, modes, LPF2.SPIKE_Ultrasonic, timer = -1, freq = 5)    # ESP
#lpf2 = LPF2.Prime_LPF2(1, 'Y1', 'Y2', modes, LPF2.SPIKE_Ultrasonic, timer = 4, freq = 5)    # PyBoard
# use EV3_LPF2 or Prime_LPF2 - also make sure to select the port type on the EV3 to be ev3-uart

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

          if value < 9:
               value = value + 1
          else:
               value = 0

          lpf2.load_payload('Int8',value)
          print(value)

          utime.sleep_ms(200)