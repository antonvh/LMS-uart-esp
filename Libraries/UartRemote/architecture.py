# This is non working code !!!
# Just sketching architecture on user side. Not everything is implemented yet.



#######  master side #######

ur=UartRemote()

# Download slave script
ur.repl_activate()
ur.repl_run("""
# some script (see slave side)
""")
# Run loop on slave, this will not REPLy.
ur.repl_run("ur.loop()", reply=False)

# send receive command
# identical to current situation, except for the extra () around encoding and payload.
reply = ur.call('my_function', 'B2s', [[1,2,3],"hi"], encoder=ur.pack, decoder=ur.unpack)
reply = ur.call('my_function', 'B2s', [[1,2,3],"hi"]) # equivalent
reply == ('my_functionack', ['hi', 'hihi', 'hihihi'])

# Custom encode/decode. Slave side only gets and sends bytes.
reply = ur.call(
    'total', 
    [1,2,3,4], 
    encode=lambda b: struct.pack('BBBB',*b), 
    decode=lambda i: struct.unpack('i',i)
    )
reply == ('totalack', 10)

# default testing command. Returns strings you throw at it.
reply = ur.call('echo', 's','hello')
reply == ('echoack', 'hello')
reply = ur.call('echo', 'B',3,5)
# Echo always returns strings
reply == ('echoack', '[3,5]')

# Turn off encoding to speed it up. Unpacker will stay default ur.unpack()
# If ur.unpack() 'excepts' because of bad formatting it stops and returns the raw bytes.
reply = ur.call('echo', b'hello', encoder=None, decoder=None)
# Echo always returns strings
reply == ('echoack', "b'hello'")
reply = ur.call('raw_echo', b'hello', encoder=None, decoder=None)
reply == ('raw_echoack', b'hello')
reply = ur.call('raw_echo', 'raw', b'hello')
reply == ('raw_echoack', b'hello')

# send command only, don't bother reveceiving and don't block.
ur.call('sleep', 'i', 2000, reply=False) 




####### slave side #######
ur=UartRemote()

def echo(*args):
    return str(args)

def raw_echo(my_bytes):
    return my_bytes

def my_function(my_list, my_str):
    return [n*my_str for n in my_list]

def total(my_encoded_list):
    my_list = struct.unpack('BBBB', my_encoded_list)
    total=sum(my_list)
    return struct.pack('i', total)

# Examples
ur.add_command(echo, 'repr')
ur.add_command(echo, 'repr', name='echo')        # equivalent
ur.add_command(my_function, 'repr')


# Void or raw return
ur.add_command(raw_echo)
ur.add_command(total)

# start loop
ur.loop()


# Create custom loop, handling any 'call()' from master
def loop():
    while True:
        # Non-blocking processing of any available calls over uart
        # Also disables local repl for convenience
        ur.process_uart()
        # Do your stuff here
        pass
    ur.enable_local_repl()
# loop()

# Alternatively get commands and their data. 
def loop():
    while True:
        # Non-blocking receipt if any available calls over uart
        # Also disables local repl for convenience
        # Auto acks receipt of call
        command, value = ur.receive_command(ack=True)
        # Do your stuff here
        if command == 'wait':
            utime.sleep_ms(value)
#loop()

# Alternatively get commands and their data and send custom reply. 
def loop():
    while True:
        # Non-blocking receipt if any available calls over uart
        # Also disables local repl for convenience
        # Auto acks receipt of call
        command, value = ur.receive_command(ack=False)
        # Do your stuff here
        if command == 'local_ticks':
            result = utime.ticks_ms()
            ur.ack_ok(command, 'I', result)
        else:
            ur.ack_err('no such command')
#loop()

# Ack_ok and ack_err are just wrappers:
def ack_ok(self, *args):
    if len(args > 1):
        self.call(args[0]+'ack', *args[1:], wait=False)
    else:
        self.call(args[0]+'ack', wait=False)

def ack_err(self, message):
    self.call('err', 's', message, wait=False)

## TODO: check wether using these wrappers limits speed. 
# So far encoding/decoding routines seem to have te biggest impact
# Payload size not so much.