# Real time 3d view of SPIKE orientation

This demo uses the angles `yaw`, `pitch`, and `roll` as output by the IMU of the SPIKE hub to plot a real time 3D presenation of the SPIKE on the PC. The movements of the real SPIKE are shown in real time on the model.

 ![plot](./pictures/imu3d_vpython.png)


## Running the demo

This project uses websockets. Therefore, the two files: `ws_connection.py` and `ws_server.py` need to be copied to the ESP8266. This can be done by using the WebREPL upload function. Then, paste the code of `imu3d_SPIKE.py` in an empty python project in the Lego Education SPKE Prime IDE. Connect the ESP8266 module (in this example it is connected to port "A"). Execute the code. The IP address of the websocket is shown in the console of the IDE.

On your PC, edit the file `imu3d_SPIKE.py` with the correct websocket address. Run the code. For installation of VPython see below.

## Websockets

The SPIKE sen

## VPython
 On the PC the 3d represenation is created using VPython. this is an easy to use 3d library. VPython uses a browser window as output terminal.

 You can install VPyhton with:

 ```
 pip3 install vpython
 ```

