# UartRemote library for Arduino

C or C++ does not have a dynamic struct pack or unpack function such as available in Python. The project [struct](https://github.com/svperbeast/struct) implements a library that provides two function `struct_pack` and `struct_unpack` which takes roughly the same parameters as the [equivalent](https://docs.python.org/3/library/struct.html#module-struct) functions in Python.

Using these functions, an Arduino library is developed which acts as the counterpart of the [MicroPython UartRemote](https://github.com/antonvh/LMS-uart-esp/tree/main/Libraries/UartRemote/MicroPython) library. Only the communication based on struct data is suppoerted by the Arduino library.

## Installing the library in Arduino

## 
