from machine import I2S, Pin
from ulab import numpy as np
from ulab import scipy as spy
import time
from uartremote import *


SCK_PIN=33
SD_PIN=32
WS_PIN=27

I2S_ID=0

alpha=0.997

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


# initialize 
#neop=neopixel.NeoPixel(Pin(21),64)

def level(l):
	for i in range(8):
		if i<l:
			neop[i]=(5*i,5*(7-i),0)
		else:
			neop[i]=(0,0,0)
		neop.write()


def led_xy(x,y,col):
    iy=y%8
    neop[iy*8+x]=col

def led_power(q):
    m=3000 #max(q)
    f=m/8
    for i,qi in enumerate(q):
        l=qi
        if l>m:
            l=m
        iy=int(l/f)
        for ii in range(iy):
            led_xy(i,ii,(30,0,0))
        for ii in range(iy,8):
            led_xy(i,ii,(0,0,0))
    neop.write()
    
    


mic_samples = bytearray(256)
mic_samples_mv = memoryview(mic_samples) # efficient pointer to original array

# we use efficient ulab functions (written in C) 
m_sq=np.zeros(5)
m_sq_prev=np.zeros(5)
alpha=0.1

def spec():
    global m_sq,m_sq_prev
    num_bytes_read_from_mic = audio_in.readinto(mic_samples_mv)
    # interpret raw buffer to signed int16 array
    q=np.frombuffer(mic_samples,dtype=np.int16)
    # multiply each array elemelt with hamming windows
    q=q*hamming(128)
    q=q-np.mean(q) # get rid of DC component
    # perform FFT and take abolute value of complex numbers
    z=spy.signal.spectrogram(q)
    # reshape only positive frequency elements in n bins
    zs=z[:60].reshape((5,12))
    # calculate sum of each bin
    sq=np.sum(zs,axis=1)
    #m_sq=np.maximum(sq,m_sq) # take maximum per array element
    m_sq=alpha*sq+(1-alpha)*m_sq_prev
    m_sq=np.maximum(sq,m_sq)
    m_sq_prev=m_sq
    return tuple(list(sq.tolist()+m_sq.tolist()))
    #return tuple(sq)


def add_commands(ur):
    ur.add_command(spec,'10f')

ur=UartRemote()
add_commands(ur)
ur.loop()