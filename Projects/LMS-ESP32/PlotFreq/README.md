# Plot Frequency Spectrum

This is a small demo that shows how to use the micophone on the LMS-esp32 board. The microphone is connected to GPIO 27, 32 and 33 as I2S_WS, I2S_SD and I2S_SCK, respectively. The microphone is sampled through the I2S and gives an array of int16 (2 bytes per sample). This needs to be converted in an numpy array.

Throughout this example we use the ulab numpy library for fast operations on arrays, and for a fast FFT implementation.

This example uses the LVGL library where the pinout is compatible with the 2.4" lcd convertor board, but any SPI TFT screen can be used. The touch capabilities are not used in this example.