from hmc5883l import HMC5883L

sensor = HMC5883L(scl=5, sda=4)
valmin=[0,0,0]
valmax=[0,0,0]
valscaled=[0,0,0]


def convert(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


f=open("cal.csv",'w')

for count in range(3000):
    valread = sensor.read()
    # for i in range(3):
    #     if valread[i]<valmin[i]: valmin[i]=valread[i]
    #     if valread[i]>valmax[i]: valmax[i]=valread[i]
    #     valscaled[i]=convert(valread[i],valmin[i],valmax[i],-100,100)
    #degrees, minutes = sensor.heading(valscaled[0], valscaled[1])
    print("%04d"%count,valmin,valmax,valread)
    f.write("%f,%f,%f\n"%valread)
f.close()
