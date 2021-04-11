# Copyright (c) 2017 Out of the BOTS
# http://outofthebots.com.au/
# Author: Shane Gingell
#
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, 
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, 
#    this list of conditions and the following disclaimer in the documentation 
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND 
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
# OR TORT INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''
Micro-Python class for ili9341 TFT.
version 5/12/2017
This is very first version without any error checking for the purposes of just 
loading a full screen image in 320x200. The image will need to have been rotated
90 degress CW and in 16bit BMP format using 5R,6G,5B format
please note that during the init of the screen it will be put into 16RBG format
and not the usual 16BGR format used by most graphic libiaries
'''

from machine import Pin, SPI
import time
import ustruct
import framebuf

class ili9341():
  
  def send_spi(self,data, is_data):
    self.dc.value(is_data)
    self.cs.value(0)
    self.hspi.write(data)
    self.cs.value(1)  
  
  def __init__(self, cs=16, dc=4):
    self.hspi = SPI(miso=Pin(12), mosi=Pin(13, Pin.OUT), sck=Pin(14, Pin.OUT),baudrate=80000000)
    self.cs = Pin(cs, Pin.OUT)
    self.dc = Pin(dc, Pin.OUT)

    for command, data in (
      (0xef, b'\x03\x80\x02'),
      (0xcf, b'\x00\xc1\x30'),
      (0xed, b'\x64\x03\x12\x81'),
      (0xe8, b'\x85\x00\x78'),
      (0xcb, b'\x39\x2c\x00\x34\x02'),
      (0xf7, b'\x20'),
      (0xea, b'\x00\x00'),
      (0xc0, b'\x23'),  # Power Control 1, VRH[5:0]
      (0xc1, b'\x10'),  # Power Control 2, SAP[2:0], BT[3:0]
      (0xc5, b'\x3e\x28'),  # VCM Control 1
      (0xc7, b'\x86'),  # VCM Control 2
      (0x36, b'\x70'),  # Memory Access Control 
      (0x3a, b'\x55'),  # Pixel Format
      (0xb1, b'\x00\x18'),  # FRMCTR1
      (0xb6, b'\x08\x82\x27'),  # Display Function Control
      (0xf2, b'\x00'),  # 3Gamma Function Disable
      (0x26, b'\x01'),  # Gamma Curve Selected
      (0xe0, b'\x0f\x31\x2b\x0c\x0e\x08\x4e\xf1\x37\x07\x10\x03\x0e\x09\x00'), # Set Gamma
      (0xe1, b'\x00\x0e\x14\x03\x11\x07\x31\xc1\x48\x08\x0f\x0c\x31\x36\x0f')):  # Set Gamma
      self.send_spi(bytearray([command]), False)
      self.send_spi(data, True) 
    self.send_spi(bytearray([0x11]), False)
    time.sleep_ms(10)
    self.send_spi(bytearray([0x29]), False)

  #do be aware this fuction swaps the width and height
  def set_window(self, x0=0, y0=0, width=320, height=240):	      
    x1=x0+width-1
    y1=y0+height-1		
    self.send_spi(bytearray([0x2A]),False)            # set Column addr command		
    self.send_spi(ustruct.pack(">HH", x0, x1), True)  # x_end 
    self.send_spi(bytearray([0x2B]),False)            # set Row addr command        
    self.send_spi(ustruct.pack(">HH", y0, y1), True)  # y_end        
    self.send_spi(bytearray([0x2C]),False)            # set to write to RAM		

  #chuck size can be increased for faster wiring to the screen at cost of RAM
  def load_image(self, image_file, chunk_size=1024):
    self.set_window(0,0,320,240)  
    BMP_file = open(image_file , "rb")
    data = BMP_file.read(54)
    data = BMP_file.read(chunk_size)
    while len(data)>0 :
      self.send_spi(data, True)
      data = BMP_file.read(chunk_size)
    BMP_file.close()

  def restore_image(self, box, image_file):     
	chunk_size = box[2] * 2     
	self.set_window(box[0], box[1], box[2], box[3])    
	BMP_file = open(image_file , "rb")     
	self.dc.value(1)     
	self.cs.value(0)
    
	for looping in range (box[3]): 	  
	  BMP_file.seek(54 + box[0] * 2 + (box[1] + looping) * 320*2, 0)      
	  data = BMP_file.read(chunk_size)      
	  self.hspi.write(data)   
	
	BMP_file.close()
	self.cs.value(1)


  def bit24_to_bit16(self, colour):
    return  (colour[2] & 0xf8) << 8 | (colour[1] & 0xfc) << 3 | colour[0] >> 3      

  def put_text(self, xpos, ypos, scale, text_graphics, background_colour, foreground_colour):     
	text_file = open ("text.fnt", "rb")  
	bk = self.bit24_to_bit16(background_colour)
	fg = self.bit24_to_bit16(foreground_colour)
	color = (ustruct.pack('>H',bk), ustruct.pack('>H',fg))
	
	for counter, charter in enumerate(text_graphics):	
	  letter = []
	  text_file.seek((ord(charter)-32)*8,0)
	  for i in range(8) : 
	    te = ustruct.unpack('B' ,text_file.read(1))
	    letter.append(te[0])
    
	  self.set_window(xpos + (8*scale* counter), ypos, 8* scale, 8 * scale)	
	  
	  self.dc.value(1)    
	  self.cs.value(0)

	  for lines in reversed(letter): 	  
	    for times in range(scale):        
		  mask = 0b10000000        
		  for bits in range(8) :		    
			if mask & lines > 0 : pos =1 		    
			else : pos = 0 		    
			self.hspi.write(color[pos]*scale) 		    
			mask = mask >> 1
	
	self.cs.value(1)
	text_file.close()
	return (xpos, ypos, len(text_graphics) * 8 * scale, 8 * scale)
	