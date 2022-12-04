# install vpython, see https://vpython.org/presentation2018/install.html



import math
import numpy as np
from vpython import *

import time
import sys,os
import websocket

# websocket initialization

websocket.enableTrace(False)
ws = websocket.WebSocket()
ws.connect("ws://192.168.x.x:80")  # replace with IP address of ESP module
ws.send("wsopen")
ws.send("euler")
ACC='acc'
EULER='euler'

# conversion

toRad = np.pi/180
toDeg = 1/toRad


# set the scene
scene.range=15
scene.forward=vector(-1,-1,-1)
scene.width=600
scene.height=600



# define fixed axes frame
xArrow=arrow(length=8,shaftwidth=.3, color=color.red, axis=vector(1,0,0))
yArrow=arrow(length=8,shaftwidth=.3, color=color.green, axis=vector(0,1,0))
zArrow=arrow(length=8,shaftwidth=.3, color=color.blue, axis=vector(0,0,1))

# define frame with axes moving with the object
frontArrow=arrow(length=4,shaftwidth=.3, color=color.purple, axis=vector(1,0,0))
upArrow=arrow(length=1,shaftwidth=.3, color=color.magenta, axis=vector(0,1,0))
sideArrow=arrow(length=2,shaftwidth=.3, color=color.orange, axis=vector(0,0,1))

# create a 'SPIKE'
bSpike=box(length=12,width=7,height=1,opacity=0.8,pos=vector(0,1,0))
bSpikebottom=box(length=12,width=7,height=3,opacity=0.8,color=color.yellow,pos=vector(0,-1,0))
bSpiktbtnL=box(length=1,width=2,height=0.01,pos=vector(5,1.5,2),color=color.white)
bSpiktbtnR=box(length=1,width=2,height=0.01,pos=vector(5,1.5,-2),color=color.white)
cSpikebtn=cylinder(radius=1,pos=vector(5,1.5,0),axis=vector(0,.01,0),color=color.white)
cSpikeblue=cylinder(radius=.5,pos=vector(-4.5,1.5,-2),opacity=0.5,axis=vector(0,.01,0),color=color.blue)

# set all in a single compounf object
Spike=compound([bSpike,bSpikebottom,bSpiktbtnL,bSpiktbtnR,cSpikebtn,cSpikeblue])

while True:
    try:
        recv=None
        while recv==None:
            recv= ws.recv()
            if recv!=None:
                s=recv.split(' ')
                cmd,value=s[0],s[1:][0]  # split result in command and value
                ret=[float(ii) for ii in value.split(',')]
                #if cmd==EULER:
                #    ret=fromeuler(*tuple(ret))
                #print(recv,ret)
        y,p,r=ret # order of values is yaw, roll, pitch
        # convert to radians
        yaw=y*toRad
        pitch=-p*toRad # change sign
        roll=-r*toRad # change sign
        # up vector as function of yaw and pitch
        # see http://planning.cs.uiuc.edu/node102.html for rotation matrices
        # take 1st column of product of yaw*pitch matrix
        #
        k=vector(cos(yaw)*cos(pitch),sin(pitch),sin(yaw)*cos(pitch))
        
        y=vector(0,1,0) # helper vector for calculating cross product
        s=cross(k,y) # perpendicular to y and k
        v=cross(s,k) # perpendicular ro s and k
        vrot=v*cos(roll)+cross(k,v)*sin(roll) # rodriguez rotation (k.v=0)

        frontArrow.axis=k
        upArrow.axis=vrot
        sideArrow.axis=cross(k,vrot)

        upArrow.length=6
        frontArrow.length=10
        sideArrow.length=6

        Spike.axis=k
        Spike.up=vrot
    except KeyboardInterrupt:
        ws.close()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
