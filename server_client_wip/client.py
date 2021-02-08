import socket
import time
import asyncio
import sys

async def gettingConnection(host,port,socket):
	socket.connect((host, port))

async def send_msg(s):
	msg = "Barrier removed, fix it, now\n"
	msg_utf = msg.encode()
	s.sendall(msg_utf)
	print("Size of Message: {0}".format(sys.getsizeof(msg_utf)))

async def gettingDataBack(socket):
	data = socket.recv(1024)
	message = data.decode() + '\n'
	print("Received Message",repr(data))
	#return message
async def main():
	HOST = '192.168.1.3' # IP address of server
	PORT = 9700

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	await gettingConnection(HOST, PORT, s)

	#Starting timer at connection to server
	time0 = time.time()
	
	# Sending message to server
	for i in range(0,100):
		await send_msg(s)

	#End timer of C->S and start timer of S->C
	#time1 = time.time()
	print("Finished Sending Message")
	

	#Calculating and printing C->S time
	#client_server_time = ((time1 - time0) * 1000)
	#print("C->S Latency: {:.2f} ms".format(client_server_time))

	# Receiving reply message from server
	await gettingDataBack(s)

	#End timer of S->C End time of round trip
	time2 = time.time()


	#Calculating and printing S->C time
	#server_client_time = ((time2 - time1) * 1000)
	#print("S->C Latency: {:.2f} ms".format(client_server_time))
	
	rtt = ((time2 - time0) * 1000)/2
	print("Total Latency: {:.2f} ms".format(rtt))
 

	s.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

