from projects.uartremote import *
ur=UartRemote('D')

print('before add_module')
print("these commands are available")
print(ur.get_remote_commands())

ur.add_module('led')
print('after add_module("led")')
print("these commands are available")
print(ur.get_remote_commands())

ur.add_module('test')
print('after add_module("test")')
print("these commands are available")
print(ur.get_remote_commands())
