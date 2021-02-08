import socket
import time
import asyncio
import sys
import csv

async def gettingConnection(host,port,socket):
	socket.connect((host, port))



async def send_msg(s):
	msg = "Staying too close to the border, move, now"
	msg_utf = msg.encode()
	s.sendall(msg_utf)

	#print("Size of Message: {0}".format(sys.getsizeof(msg_utf)))

async def gettingDataBack(socket):
	data = socket.recv(1024)
	message = data.decode('utf-8','replace')
	print("Size of Message: {0}".format(sys.getsizeof(message)))
	print("Received Message: ", message[2:]) #Removing tab and ascii character that is added for some reason TODO
	#return message


	


async def main():


	#Starting timer at connection to server
		
	# Sending message to server
	with open('latency2GHz-outdoorrunning-newrouter-12-23-93B-60m-insurance-routermovedback.csv','w') as f1:
		writer=csv.writer(f1, delimiter='\t',lineterminator='\n',)
		for i in range(0,500):
			HOST = '192.168.0.142' # IP address of server
			PORT = 9700
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			await gettingConnection(HOST, PORT, s)
			time0 = time.time()		
			await send_msg(s)
			await gettingDataBack(s)
			time1 = time.time()
			rtt = ((time1 - time0) * 1000)/2
			print("Total Latency: {:.2f} ms".format(rtt))
			print(i)
			row = [rtt]
			writer.writerow(row)
			s.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

