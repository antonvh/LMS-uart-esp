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

spike_code="import ubinascii, uos, machine\nb64=\"\"\""+ur_b64.decode('utf-8')+"\"\"\"\n\n"
spike_code+="""
uartremote=ubinascii.a2b_base64(b64)

try:
    uos.remove('/projects/uartremote.py')
    uos.remove('/projects/uartremote.mpy')
except OSError:
    pass

print('writing uartremote.mpy to folder /projects')
print('writing uartremote.mpy to folder /projects')
f=open('/projects/uartremote.mpy','wb')
f.write(uartremote)
f.close()
print('Finished writing uartremote.mpy. Resetting.')
machine.reset()
"""

open('install_uartremote.py','w').write(spike_code)