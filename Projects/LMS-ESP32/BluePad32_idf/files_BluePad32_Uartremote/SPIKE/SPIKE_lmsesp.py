from projects.uartremote import *
from utime import sleep_ms,ticks_ms,ticks_diff
import time
import hub
u=UartRemote("B")

class LMSESP:
   def __init__(self, ur):
      self.ur=ur
      
   def gamepad_connected(self):
       ack,connected=self.ur.call('connected')
       return connected
    
   def gamepad(self):
      ack,gp=self.ur.call('gamepad')
      try:
          buttons,dpad,left_joy_x,left_joy_y,right_joy_x,right_joy_y=gp
      except:
          buttons,dpad,left_joy_x,left_joy_y,right_joy_x,right_joy_y =(0,0,0,0,0,0)
      # process buttone etc.
      btns=get_button(buttons,dpad)
      #btns=[]
      return (btns,left_joy_x,left_joy_y,right_joy_x,right_joy_y)
   
   def gamepad_led(self,leds):
       ack,resp=self.ur.call('led','B',leds)
       
       
   def gamepad_rumble(self,rumble_force,rumble_duration):
       ack,resp=self.ur.call('rumble','2B',rumble_force,rumble_duration)
   
   def neopixel(self,led_nr,r,g,b):
      ack,np=self.ur.call('neopixel','4B',led_nr,r,g,b)

   def neopixel_show(self):
      ack,nps=self.ur.call('neopixel_show')
      
   def neopixel_init(self,nr_leds,pin):
      ack,npi=self.ur.call("neopixel_init","2B",nr_leds,pin)
      
   def i2c_scan(self):
      ack,resp=self.ur.call('i2c_scan')
      try:
          dev=[i for i in resp[1]]
          return dev
      except:
          return []
      
   def i2c_read(self,addr,nr_bytes):
       ack,resp=self.ur.call('i2c_read','2B',addr,nr_bytes)
       return resp
    
   #def i2c_write ...

   def servo(self,servo_nr,angle):
      ur,se=self.ur.call('servo','>Bi',servo_nr,angle)
 
 
   def audio(self):
      ur,level=self.ur.call('audio')
      return level
    
    
def get_button(buttons,dpad):
    btns=[]
    if buttons & 2:
        btns.append('A')
    if buttons & 1:
        btns.append('B')
    if buttons & 4:
        btns.append('Y')
    if buttons & 8:
        btns.append('X')
    if buttons & 16:
        btns.append('L')
    if buttons & 64:
        btns.append('ZL')
    if buttons & 32:
        btns.append('R')
    if buttons & 128:
        btns.append('ZR')
    if dpad & 1 :
        btns.append('DU')
    if dpad & 2 :
        btns.append('DD')
    if dpad & 4 :
        btns.append('DR')
    if dpad & 8 :
        btns.append('DL')
    return btns               
   
     
    
"""
from uartremote import *
from SPIKE_lmsesp import LMSESP

ur=UartRemote('A')
lmsesp=LMSESP(u)

lmsesp.neopixel(1,20,0,0)
lmsesp.neopixel(2,0,30,0)
lmsesp.neopixel_show()

while True:
    btns,left_joy_x,left_joy_y,right_joy_x,right_joy_y=lmsesp.gamepad()
    lmsesp.servo(2,int((left_joy_x+512)/1024*180))

while True:
    btns,left_joy_x,left_joy_y,right_joy_x,right_joy_y=lmsesp.gamepad()
    if len(btns)>0:
      print(btns)


while True:
    ack,gp=u.call('gamepad')
    left_joy_x=gp[2]
    ack,resp=u.call('servo','>BI',2,int((left_joy_x+512)/1024*180))

i2c_devices=lmsesp.i2c_scan()
read_ana_joy=lmsesp.i2c_read(0x52,3)

audio_level=lmssp.audio()
"""

