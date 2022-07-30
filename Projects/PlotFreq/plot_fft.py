from machine import I2S,Pin
import time
import espidf as esp
from ulab import numpy as np
from ulab import scipy as spy
import lvgl as lv
from ili9XXX import ili9341,LANDSCAPE
disp = ili9341( miso=12, mosi=13, clk=14, cs=15, dc=23, rst=25, backlight=-1,power=-1,width=320, height=240, rot=LANDSCAPE)

# touch sensor is on the same SPI bus as the display
from xpt2046 import xpt2046
touch = xpt2046(spihost=esp.HSPI_HOST,cs=26,transpose=False,cal_x0=3865, cal_y0=329, cal_x1=399, cal_y1=3870)

# this is only needed when Pin(2) is connected to the background display
from machine import Pin
l=Pin(2,Pin.OUT)
l.value(1)

#define I2S pins
SCK_PIN=33
SD_PIN=32
WS_PIN=27

I2S_ID=0

WAV_SAMPLE_SIZE_IN_BITS = 16
FORMAT = I2S.MONO
SAMPLE_RATE_IN_HZ = 5000 # up to 2500Hz, enough for voice
BUFFER_LENGTH_IN_BYTES = 4192

audio_in=I2S(I2S_ID,
             sck=Pin(SCK_PIN),
             ws=Pin(WS_PIN),
             sd=Pin(SD_PIN),
             mode=I2S.RX,bits=16,
             format=FORMAT,
             rate=SAMPLE_RATE_IN_HZ,
             ibuf=BUFFER_LENGTH_IN_BYTES)


def hamming(N):
    # hamming filter for removing sharp artefacts of finite sampling signal
    n=np.linspace(0,N,num=N)
    w=0.54-0.46*np.cos(2*3.1415*n/N)
    return w




# memoryview is used here for increased performance
mic_samples = bytearray(512)
mic_samples_mv = memoryview(mic_samples) # efficient pointer to original array

# we use efficient ulab functions (written in C) 
sq=np.zeros(64)
z=np.zeros(128)

def spec():
    global z
    num_bytes_read_from_mic = audio_in.readinto(mic_samples_mv)
    # interpret raw buffer to signed int16 array
    q=np.frombuffer(mic_samples,dtype=np.int16)
    # multiply each array element with hamming window
    q=q*hamming(256)
    # perform FFT and take abolute value of complex numbers
    # spy.signal.spectorogram does this in one go
    z=spy.signal.spectrogram(q)[:128]
    # reshape only positive frequency elements in n bins
    #zs=z[64:64+60].reshape((5,12))
    # calculate sum of each bin
    #sq=np.sum(zs,axis=1)
    #zs=z[64:64+60]
    # calculate sum of each bin
    
def freq():
    ll=32768
    ls=256
    num_bytes_read_from_mic = audio_in.readinto(mic_samples_mv)
    # interpret raw buffer to signed int16 array
    q=np.frombuffer(mic_samples,dtype=np.int16)
    # multiply each array elemelt with hamming windows
    q=q*hamming(256)
    ql=np.concatenate((q,np.zeros(ll-ls)))
    z=spy.signal.spectrogram(ql)
    ii=np.argmax(z)
    return(ii*SAMPLE_RATE_IN_HZ/ll)
    

q=np.zeros(128,dtype=np.int16)

def get_sample():
    global q
    num_bytes_read_from_mic = audio_in.readinto(mic_samples_mv)
    q=np.frombuffer(mic_samples,dtype=np.int16)
                   
# this is a dummy function used for converting to np.int16
def f(x):
   return int(x)

vf=np.vectorize(f,otypes=np.int16)


chart = lv.chart(lv.scr_act())
chart.set_size(300, 200)
chart.center()
chart.set_type(lv.chart.TYPE.LINE)   # Show lines and points too
chart.set_point_count(128)
# define series 1 
ser1 = chart.add_series(lv.palette_main(lv.PALETTE.RED), lv.chart.AXIS.PRIMARY_Y)
  
    
def plot():
    chart.set_range(lv.chart.AXIS.PRIMARY_Y, min(q),max(q))
    chart.set_range(lv.chart.AXIS.PRIMARY_X, 0,128)
    ser1.y_points = q
    chart.refresh()    

def plot_spec():
    q=vf(z)
    chart.set_range(lv.chart.AXIS.PRIMARY_Y, min(q),max(q))
    chart.set_range(lv.chart.AXIS.PRIMARY_X, 0,128)
    ser1.y_points = q
    chart.refresh()    

   
while True:
  spec()
  plot_spec()

