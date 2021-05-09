import ubinascii, uos, machine
b64="""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
"""


uartremote=ubinascii.a2b_base64(b64)

try:
    uos.remove('/projects/uartremote.py')
    uos.remove('/projects/uartremote.mpy')
except OSError:
    pass

print('writing uartremote.mpy to folder /projects')
print('writing uartremote.mpy to folder /projects')
open('/projects/uartremote.mpy','wb').write(uartremote)
print('Finished writing uartremote.mpy')
machine.reset()
