# This is non working code !!!
# Just some usage examples.



#######  master side #######

ur=UartRemote()

# Download slave script
ur.repl_activate()
ur.repl_run("""
# some micropython script that runs on on slave (see slave side)
""")
# Run loop on slave, this will not REPLy.
ur.repl_run("ur.loop()", reply=False)

# send receive command, using repr is the easiest
reply = ur.call('my_function', 'repr', [1,2,3], "hi")
reply == ('my_functionack', ['hi', 'hihi', 'hihihi'])

# You can also use struct.pack like format strings
# But the you can only use int, string and float (no list etc...)
# This is a bit faster, though.
reply = ur.call('some function', 'BBB2sf', 1,2,3, "hi", 5.7)
reply = ur.call('some function', '3B2sf', 1,2,3, "hi", 5.7)

# default testing command. Returns strings you throw at it.
reply = ur.call('echo', 'repr','hello')
reply == ('echoack', 'hello')
reply = ur.call('echo', 'BB',3,5)
# Echo always returns repr objects
reply == ('echoack', (3,5))

# Turn off encoding to speed it up. Unpacker will stay default ur.unpack()
# If ur.unpack() 'excepts' because of bad formatting it stops and returns the raw bytes.
reply = ur.call('echo', b'hello')
# Echo always returns using repr, but this doesn't matter here
reply == ('echoack', "b'hello'")

# Raw echo returns bytes, no format.
reply = ur.call('raw_echo', b'hello')
reply == ('raw_echoack', b'hello')

# Adding raw is is redundant, but easy to read.
reply = ur.call('raw_echo', 'raw', b'hello')
reply == ('raw_echoack', b'hello')

# send command only, don't bother receiving and don't block program execution.
ur.call('sleep', 'i', 2000, reply=False) 


####### slave side #######
# Example slave micropython script:
ur=UartRemote()

# Echo is actually an internal method in the UartRemote
def echo(*args):
    return args

def raw_echo(my_bytes):
    return my_bytes

def my_function(my_list, my_str):
    return [n*my_str for n in my_list]

def total(my_encoded_list):
    my_list = struct.unpack('BBBB', my_encoded_list)
    total=sum(my_list)
    return struct.pack('i', total)

# Examples of add command with return value format.
ur.add_command(echo, 'repr')
# equivalent, name is deduced from function name
ur.add_command(echo, 'repr', name='echo')
ur.add_command(my_function, 'repr')

# Void or raw return
ur.add_command(raw_echo)
ur.add_command(total)

# start loop
ur.loop()

## End of basic slave code


### Custom slave loops ###
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
        # WARNING: Autoack Not implemented yet. (only in dev branch)
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
# WARNING: ack_ok Not implemented yet. (only in dev branch)
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
