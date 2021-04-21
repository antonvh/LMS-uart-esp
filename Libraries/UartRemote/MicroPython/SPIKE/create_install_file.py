import binascii
uartremote=open('../uartremote.py','rb').read()
ur_b64=binascii.b2a_base64(uartremote)

spike_code="import ubinascii\nb64=\"\"\""+ur_b64.decode('utf-8')+"\"\"\"\n\n"
spike_code+="uartremote=ubinascii.a2b_base64(b64)\n\n"
spike_code+="print('writing uartremote.py to folder /projects')\n"
spike_code+="open('/projects/uartremote.py','wb').write(uartremote)\n"
spike_code+="print('Finished writing uartremote.py')\n"

open('install_uartremote.py','w').write(spike_code)