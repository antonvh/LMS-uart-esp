import binascii
uartremote=open('uartremote.mpy','rb').read()
ur_b64=binascii.b2a_base64(uartremote)

spike_code="import ubinascii\nb64=\"\"\""+ur_b64.decode('utf-8')+"\"\"\"\n\n"
spike_code+="uartremote=ubinascii.a2b_base64(b64)\n\n"
spike_code+="print('writing uartremote.mpy to folder /projects')\n"
spike_code+="open('/projects/uartremote.mpy','wb').write(uartremote)\n"
spike_code+="print('Finished writing uartremote.mpy')\n"

open('install_uartremote_mpy.py','w').write(spike_code)
