import socket

def retBanner(ip, port):
	try:
		socket.setdefaulttimeout(2)
		s = socket.socket()
		s.connect((ip, port))
		banner = s.recv(1024)
		return banner
	except:
		return
def showBanner(banner):
	print banner
def main():
	for x in range(36,255):
		ip = "192.168.50." + str(x)
		for port in range(20,65535):
			banner = retBanner(ip, port)
			if banner:
				print '[+] ' + ip + ': ' + str(port) + 'y'
				showBanner(banner)
			#else:
			#	print '[+] ' + ip + ': ' + str(port) + 'n'
if __name__ == '__main__':
	main()
