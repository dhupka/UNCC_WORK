import socket
import time
import asyncio
import sys

async def send_msg(conn, msg):
	conn.sendall(msg)

async def main():
	HOST = '192.168.1.2' #'192.168.0.100' # IP address of current device
	# To get IP address, run ifconfig in terminal, IP will be the inet returned from ifconfig
	PORT = 9700

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	s.bind((HOST, PORT))
	s.listen(5)

	conn, addr = s.accept()
	time0 = time.perf_counter()
	print('Connected by', addr)

	for i in range(0,100):
		while True:
			data = conn.recv(4096)
			#time1 = time.perf_counter()
			print(type(data))
			print("Received Message: {0}",repr(data))
			#print("Size of Message: {0}".format(sys.getsizeof(data)))

			#server2client_time = ((time1 - time0) * 1000)
			#print("S->C Latency: {:.2f} ms".format(server2client_time))
			if not data:
				break
		
		message = data.decode() + '\n'
		#await send_msg(conn, message.encode())
		#time2 = time.perf_counter()

		#msg = "Hello, world\n"
		#msg_utf = msg.encode()
		#conn.sendall(msg_utf)

		#client2server_time = ((time2 - time1) * 1000)
		#print("C->S Latency: {:.2f} ms".format(client2server_time))

		
		time3 = time.perf_counter()
		total_time = ((time3 - time0) * 1000) / 2
		print("Total Latency: {:.2f} ms".format(total_time))

	conn.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

