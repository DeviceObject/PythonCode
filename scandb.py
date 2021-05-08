class DataInterface:
    server_ip = ""
    server_port = 0
    def __init__(self, ip, port):
        self.server_ip = ip
        self.server_port = port
    def connect(self):
        print("connect " + self.server_ip + " " + str(self.server_port))
    def disconnect(self):
        print("disconnect " + self.server_ip + " " + str(self.server_port))
        
class mysqldb_interface(DataInterface):
    server_ip = "localhost"
    server_port = 3306
    def __init__(self):
        return
    def __init__(self, ip, port):
        DataInterface.__init__(self, ip, port)
    def connect(self):
        print("connect mysql server")
    def disconnect(self):
        print("disconnect mysql server")
        