"""

fake server for testing the denso client.

"""

import socket

IP = 'localhost'
PORT = 5005
BUFFER_SIZE = 256

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP, PORT))
s.listen(1)

conn, addr = s.accept()

print 'CONNECTION:', addr
while 1:
	data = conn.recv(BUFFER_SIZE)
	if data == 'CLOSE':
		break
	print "MSG: %s" % data
	try:
		conn.send("DONE")
	except socket.error as e:
		break
conn.close()