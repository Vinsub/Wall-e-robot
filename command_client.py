import socket                # Import socket module

s = socket.socket()        # Create a socket object
host = "localhost" 	# Get local machine name
port = 5001             	# Reserve a port for your command service

s.connect((host, port))
print "Connect to " + host
print "Use f for detection, 4, 5, r, t for manual command of the head, q to quit "
while (True):
    command = raw_input ("Command? ")
    s.send(command)
    print s.recv(1024)
    if command == "q":
        break
s.close                     # Close the socket when "q"
