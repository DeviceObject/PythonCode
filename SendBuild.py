import os
import socket

def entry():
    Socket = socket.socket()
    RemoteHost = socket.gethostname() #"127.0.0.1"
    RemotePort = 8888
    
    Socket.connect((RemoteHost,RemotePort))
    
    SignatureCode = "Mbr" + ","
    CommandType = "Generate" + ","
    InitCodeUrl = "http://www.bioskit.com/" + ","
    RunCodeUrl = "http://www.bioskit.com/" + ","
    
    Version = "Windows x64"
    
    SendDat = SignatureCode + CommandType + InitCodeUrl + RunCodeUrl
    print('Online:',str(SendDat))
    Socket.send(SendDat)
    pdat = Socket.recv(1024)
    print(pdat)
    Socket.close()
    
if __name__ == "__main__":
    entry()

