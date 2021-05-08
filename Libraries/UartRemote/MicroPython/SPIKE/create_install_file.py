#!python3

# Run this on a Mac or Linux machine to create/update 'install_uartremote.py'
# Copy the contents of install_uartremote.py into an empty SPIKE Prime project
# And run to install

import binascii, mpy_cross, time

mpy_cross.run('-march=armv6','../uartremote.py','-o','uartremote.mpy')

# Should be done in a second!
time.sleep(1)

uartremote=open('uartremote.mpy','rb').read()
ur_b64=binascii.b2a_base64(uartremote)

spike_code="import ubinascii\nb64=\"\"\""+ur_b64.decode('utf-8')+"\"\"\"\n\n"
spike_code+="uartremote=ubinascii.a2b_base64(b64)\n\n"
spike_code+="print('writing uartremote.mpy to folder /projects')\n"
spike_code+="open('/projects/uartremote.mpy','wb').write(uartremote)\n"
spike_code+="print('Finished writing uartremote.mpy')\n"

open('install_uartremote.py','w').write(spike_code)