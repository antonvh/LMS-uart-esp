from projects.uartremote import *
from time import sleep_ms

SOFTRESET="""
from machine import soft_reset
soft_reset()
"""

MAINPY="""
from vl53_ESP import *
"""

ur=UartRemote("A") # connect ESP to port A


ur.flush() # remove evernything
# try to enable repl if esp is still in non_repl mode
ur.send_command("enable repl",'s','ok')
print("response enable repl",ur.uart.read(1024))

ur.repl_activate()

print(ur.repl_run("print('Repl Tested')"))
print(ur.repl_run(SOFTRESET))
sleep_ms(300)
print(ur.repl_run(MAINPY,reply=False))
print(ur.uart.read(1024))
print("loaded script")



# wait some time before sending uartremote commands
sleep_ms(1000)
print(ur.call('echo','s','Echo back from ESP'))


while True:
    print(ur.call('vl53'))
    sleep_ms(100)

