'''
LEGO SPIKE Prime Backpacks
LPF2 class allows communication between LEGO SPIKE Prime and LEGO Backpacks
Version Date: 01/06/2020
Tufts Center for Engineering Education and Outreach
Tufts University

Updated on: 01/06/2020
'''
import machine, utime, gc
import math, struct
import utime
import binascii

from machine import Timer
BYTE_NACK = 0x02
BYTE_ACK = 0x04
CMD_Type = 0x40   # @, set sensor type command
CMD_Select = 0x43   #  C, sets modes on the fly
CMD_Mode = 0x49   # I, set mode type command
CMD_Baud = 0x52   # R, set the transmission baud rate
CMD_Vers = 0x5F   # _,  set the version number
CMD_ModeInfo = 0x80  # name command
CMD_Data  = 0xC0  # data command

CMD_LLL_SHIFT = 3

NAME,RAW,Pct,SI,SYM,FCT, FMT = 0x0,0x1,0x2,0x3,0x4,0x5, 0x80
DATA8,DATA16,DATA32,DATAF = 0,1,2,3  # Data type codes
ABSOLUTE,RELATIVE,DISCRETE = 16,8,4
WeDo_Ultrasonic, SPIKE_Color, SPIKE_Ultrasonic = 35, 61, 62
Ev3_Utrasonic = 34

length = {'Int8' : 1, 'uInt8' : 1, 'Int16' : 2, 'uInt16' : 2, 'Int32' : 4, 'uInt32' : 4, 'float' : 4}
format = {'Int8' : '<b', 'uInt8' : '<B', 'Int16' : '<h', 'uInt16' : '<H', 
     'Int32' : '<l', 'uInt32' : '<L', 'float' : '>f'}

# Name, Format [# datasets, type, figures, decimals], 
# raw [min,max], Percent [min,max], SI [min,max], Symbol, functionMap [type, ?], view
mode0 = ['LPF2-DETECT',[1,DATA8,3,0],[0,10],[0,100],[0,10],'',[ABSOLUTE,0],True]
mode1 = ['LPF2-COUNT',[1,DATA32,4,0],[0,100],[0,100],[0,100],'CNT',[ABSOLUTE,0],True]
mode2 = ['LPF2-CAL',[3,DATA16,3,0],[0,1023],[0,100],[0,1023],'RAW',[ABSOLUTE,0],False]
defaultModes = [mode0,mode1,mode2]     

def log2(x):
    return math.log(x)/math.log(2)


log2val={1:0,2:1,4:2,8:3,16:4,32:5}

def log2lookup(val):
  if val in log2val:
       return log2val[val]
  else:
       return 0

def mode(name,size = 1, type=DATA8, format = '3.0',  raw = [0,100], percent = [0,100],  SI = [0,100], symbol = '', functionmap = [ABSOLUTE,0], view = True):
          fig,dec = format.split('.')
          fred = [name, [size,type,int(fig),int(dec)],raw,percent,SI,symbol,functionmap,view]
          return fred
               
class LPF2(object):
     def __init__(self, uartChannel, txPin, rxPin, modes = defaultModes, type = WeDo_Ultrasonic, timer = 4, freq = 5):
          self.txPin = txPin
          self.rxPin = rxPin
          self.uart = machine.UART(uartChannel)
          self.txTimer = timer
          self.modes = modes
          self.current_mode = 0
          self.type = type
          self.connected = False
          self.payload = bytearray([])
          self.freq = freq
          self.oldbuffer =  bytes([])
          self.textBuffer = bytearray(b'                ')
          
# -------- Payload definition

     def load_payload(self, type, array):   # note it must be a power of 2 length          
          if isinstance(array,list):
               bit = math.floor(log2(length[type]*len(array)))  
               bit = 4 if bit > 4 else bit     # max 16 bytes total (4 floats)
               array = array[:math.floor((2**bit)/ length[type])]     # max array size is 16 bytes
               value = b''
               for element in array:
                    value += struct.pack(format[type], element)
          else:
               bit = int(log2(length[type]))
               value = struct.pack(format[type], array)
               #print("load_payload",bit,value)
          payload = bytearray([CMD_Data | (bit << CMD_LLL_SHIFT) | self.current_mode])+value
          self.payload = self.addChksm(payload)
          
#----- comm stuff

     def readchar(self):
          c=self.uart.read(1)
          cbyte=ord(c) if c else -1 
          return cbyte

     def hubCallback(self, timerInfo):
          if self.connected:
               chr =self.readchar()     # read in any heartbeat bytes
               # print("cb",chr)
               while chr>=0:
                    if chr == 0:   # port has nto been setup yet
                         pass
                    elif chr == BYTE_NACK:     # regular heartbeat pulse
                         pass   
                    elif chr == CMD_Select:    # reset the mode
                         mode = self.readchar()
                         cksm = self.readchar()
                         if cksm == 0xff ^ CMD_Select ^ mode:
                              self.current_mode = mode
                              print("change mode=",mode)
                    elif chr == 0x46:     # sending over a string
                         print("string")
                         zero = self.readchar()
                         b9 = self.readchar()
                         ck = 0xff ^ zero ^ b9
                         if ((zero == 0) & (b9 == 0xb9)):   # intro bytes for the string
                              char = self.readchar()    # size and mode
                              size = 2**((char & 0b111000)>>3)
                              mode = char & 0b111
                              ck = ck ^ char
                              for i in range(len(self.textBuffer)):
                                   self.textBuffer[i] = ord(b' ')
                              for i in range(size):
                                   self.textBuffer[i] = self.readchar()
                                   ck = ck ^ self.textBuffer[i]
                              print(self.textBuffer)
                              cksm = self.readchar()
                              if cksm == ck:
                                   pass
                    # elif chr<=0x7c and (chr & 0x44) == 0x44:     # write command?
                    #      l=(chr& 0b111000)>>3
                    #      print('write chr,l',chr,l)
                    #      chk=0
                    #      s=""
                    #      for i in range(l):
                    #           thing = self.readchar()
                    #           s+=chr(thing)
                    #           chk=chk^thing
                    #      cksm = self.readchar()
                    #      if cksm == 0xff ^ 0x4C ^ chk:
                    #           pass
                    else:
                         pass
                         print("Unexpected callback from hub",chr)
                    chr = self.readchar()
                    
               size = self.writeIt(self.payload)    # send out the latest payload
               if not size: self.connected = False

     def writeIt(self,array):
          #print(binascii.hexlify(array))
          return self.uart.write(array)

     def waitFor (self, char, timeout = 2):
          starttime = utime.time()
          currenttime = starttime
          status = False
          while (currenttime-starttime) < timeout:
               utime.sleep_ms(5)
               currenttime = utime.time()
               if self.uart.any() > 0:
                    data = self.uart.read(1)
                    #print("received",data)
                    if  data == char:
                         status = True
                         break
          return status

     def addChksm(self,array):
          chksm = 0
          for b in array:
               chksm ^= b
          chksm ^= 0xFF
          array.append(chksm)  
          return array

# -----  Init and close
          
     def init(self):
          self.tx = machine.Pin(self.txPin, machine.Pin.OUT)
          self.rx = machine.Pin(self.rxPin, machine.Pin.IN)
          self.tx.value(0)
          utime.sleep_ms(500)
          self.tx.value(1)
          self.uart.init(baudrate=115200, bits=8, parity=None, stop=1)
          self.writeIt(b'\x00')

     def close(self):
          #self.uart.deinit()
          self.sendTimer.deinit()
          self.connected = False

# ---- settup definitions 
          
     def setType(self,sensorType):
          return self.addChksm(bytearray([CMD_Type, sensorType]))

     def defineBaud(self,baud):
          rate = baud.to_bytes(4, 'little')
          return self.addChksm(bytearray([CMD_Baud]) + rate) 

     def defineVers(self,hardware,software):
          hard = hardware.to_bytes(4, 'big')
          soft = software.to_bytes(4, 'big')
          return self.addChksm(bytearray([CMD_Vers]) + hard + soft)
          
     def padString(self,string, num, startNum):
          reply = bytearray([startNum])  # start with name
          reply += string
          exp = math.ceil(log2(len(string))) if len(string)>0 else 0  # find the next power of 2
          size = 2**exp
          exp = exp<<3
          length = size - len(string)
          for i in range(length):
               reply += bytearray([0])
          return self.addChksm(bytearray([CMD_ModeInfo | exp | num]) + reply)

     def buildFunctMap(self,mode, num, Type):
          exp = 1 << CMD_LLL_SHIFT
          mapType = mode[0]
          mapOut = mode[1]
          return self.addChksm(bytearray([CMD_ModeInfo | exp | num, Type, mapType, mapOut]))

     def buildFormat(self,mode, num, Type):
          exp = 2 << CMD_LLL_SHIFT
          sampleSize = mode[0] & 0xFF
          dataType = mode[1] & 0xFF
          figures = mode[2] & 0xFF
          decimals = mode[3] & 0xFF
          return self.addChksm(bytearray([CMD_ModeInfo | exp | num, Type, sampleSize, dataType,figures,decimals]))
     
     def buildRange(self,settings, num, rangeType):
          exp = 3 << CMD_LLL_SHIFT
          minVal = struct.pack('<f', settings[0])
          maxVal = struct.pack('<f', settings[1])
          return self.addChksm(bytearray([CMD_ModeInfo | exp | num, rangeType]) + minVal + maxVal)

     def defineModes(self,modes):
          length = (len(modes)-1) & 0xFF
          views = 0
          for i in modes:
               if (i[7]):
                    views = views + 1
          views = (views - 1) & 0xFF
          return self.addChksm(bytearray([CMD_Mode, length, views]))
          
     def setupMode(self,mode,num):
          self.writeIt(self.padString(mode[0],num,NAME))        # write name
          self.writeIt(self.buildRange(mode[2], num, RAW))      # write RAW range
          self.writeIt(self.buildRange(mode[3], num, Pct))        # write Percent range
          self.writeIt(self.buildRange(mode[4], num, SI))          # write SI range
          self.writeIt(self.padString(mode[5],num,SYM))          # write symbol
          self.writeIt(self.buildFunctMap(mode[6],num, FCT)) # write Function Map
          self.writeIt(self.buildFormat(mode[1],num, FMT))     # write format
          
# -----   Start everything up

     def initialize(self):
          self.connected = False
          self.sendTimer = Timer(-1)  # default is 200 ms
          self.period=int(1000/self.freq)
          self.init()
          self.writeIt(self.setType(self.type))  # set type to 35 (WeDo Ultrasonic) 61 (Spike color), 62 (Spike ultrasonic)
          self.writeIt(self.defineModes(self.modes))  # tell how many modes 
          self.writeIt(self.defineBaud(115200))
          self.writeIt(self.defineVers(2,2))
          num = len(self.modes) - 1
          for mode in reversed(self.modes):
               self.setupMode(mode,num)
               num -= 1
               utime.sleep_ms(5)
               
          self.writeIt(b'\x04')  #ACK
          # Check for ACK reply
          self.connected = self.waitFor(b'\x04')
          print('Success' if self.connected else 'Failed')

          # Reset Serial to High Speed
          # pull pin low
          #self.uart.deinit()
          if self.connected:
               tx = machine.Pin(self.txPin, machine.Pin.OUT)
               tx.value(0)
               utime.sleep_ms(10)
               
               #change baudrate
               self.uart.init(baudrate=115200, bits=8, parity=None, stop=1)
               self.load_payload('uInt8',0)
          
               #start callback  - MAKE SURE YOU RESTART THE CHIP EVERY TIME (CMD D) to kill previous callbacks running
               self.sendTimer.init(period=self.period, mode=Timer.PERIODIC, callback= self.hubCallback)   
          return

class ESP_LPF2(LPF2):
    def init(self):
          self.tx = machine.Pin(self.txPin, machine.Pin.OUT)
          self.rx = machine.Pin(self.rxPin, machine.Pin.IN)
          self.tx.value(0)
          utime.sleep_ms(500)
          self.tx.value(1)
          self.uart.init(baudrate=2400, bits=8, parity=None, stop=1)
          self.writeIt(b'\x00')

class Prime_LPF2(LPF2):
     def init(self):
          self.tx = machine.Pin(self.txPin, machine.Pin.OUT)
          self.rx = machine.Pin(self.rxPin, machine.Pin.IN)
          self.tx.value(0)
          utime.sleep_ms(500)
          self.tx.value(1)
          self.uart.init(baudrate=2400, bits=8, parity=None, stop=1)
          self.writeIt(b'\x00')

     
class EV3_LPF2(LPF2):
     def init(self):
          self.uart.init(baudrate=2400, bits=8, parity=None, stop=1)
          self.writeIt(b'\x00')

     def defineVers(self,hardware,software):
          return bytearray([])