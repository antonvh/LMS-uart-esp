# Install uartremote.py on SPIKE
## Background
The SPIKE IDE checks the filesystem of the Spike Prime. If it sees any non-system files in the root dircetory, it triggeres a firmware update. After the firmware update, the non-system files will be deleted. However, files that reside in the `/project`  will not be deleted after a firmware upgrade.
== Installation
Open a new Python project in the LEGO Education SPIKE Prime IDE and past the content of the file `install_uartremote.py` that can be found in this directory. Execute the script. Open the console in the IDE. after executing it should show

```
[18:08:28.990] > writing uartremote.py to folder /projects
[18:08:29.323] > Finished writing uartremote.py
```

the timestanps will be different on your system.

Now the uartremote.py library is copied to the `/project` directory. To use the library inlude the following line in your python code:

```from project.uartremote import *```
