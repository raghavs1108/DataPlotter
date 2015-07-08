import socket
import sys
import traceback

HOST = '10.182.0.111'   # Symbolic name, meaning all available interfaces
PORT = 8080 # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print 'Socket created'
#Bind socket to local host and port
try:
	s.bind((HOST, PORT))
except socket.error as msg:
	print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()
	print 'Socket bind complete'
#Start listening on socket
s.listen(10)
print 'Socket now listening'

#now keep talking with the client
while 1:
	#wait to accept a connection - blocking call
	conn, addr = s.accept()
	print 'Connected with ' + addr[0] + ':' + str(addr[1])
	data = conn.recv(20000)
	conn.send("recieved")
	if data == "capture" or data == "[capture\n]" or data == "['capture\n']":
		f = open("stepdata.txt", "w")
		f.write(data+"\n")
		f.close()
		print "capture recieved.\n"
	else:		    	
		data = data.split(";")
			# print data

		f = open("stepdata.txt", "w")
		for i in data:
			try:
				x = i.split("#")[0]
				y = i.split("#")[1]
				f.write(y+"\n")
			except Exception as ex:
				template = "An exception of type {0} occured. Arguments:\n{1!r}"
				message = template.format(type(ex).__name__, ex.args)
				print message
		f.close()
	conn.close()
s.close()