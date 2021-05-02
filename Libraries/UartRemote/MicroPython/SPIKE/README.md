# Install uartremote library on the SPIKE
## Background
The SPIKE IDE checks the filesystem of the Spike Prime. If it sees any non-system files in the root directory, it triggeres a firmware update. After the firmware update, the non-system files will be deleted. However, files that reside in the `/project`  will not be deleted after a firmware update.
## Installation of uartremote.py or uartremote.mpy
Open a new Python project in the LEGO Education SPIKE Prime IDE and paste in the content of the file `install_uartremote.py` that can be found in this directory. Execute the script. Open the console in the IDE. After executing it should show:

```
[18:08:28.990] > writing uartremote.py to folder /projects
[18:08:29.323] > Finished writing uartremote.py
```

The timestanps will be different on your system.

Now the uartremote.py library is copied to the `/project` directory.

The file `install_uartremote_mpy.py` does the same thing as described above, except that it installs the compiled version `uartremote.mpy` to the `/projects` directory. The compiled version will use less RAM memory when loaded and thus leaving more space for other code on the SPIKE.

 To use the library inlude the following line in your python code:

```from project.uartremote import *```
