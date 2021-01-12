# encoding=utf-8
import socket
import psutil
import time

class Client:
    SOCKET = None
    BUFFER_SIZE = 102400
    PORT = 12349

    def open(self):
        self.SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def bind(self, _port):
        self.SOCKET.bind(("", _port))

    def send(self, request, _ip, _port):
        self.SOCKET.sendto(request.encode('utf-8'), (_ip, _port))

    def recv(self):
        recv_data = self.SOCKET.recvfrom(self.BUFFER_SIZE)
        return recv_data

    def close(self):
        self.SOCKET.close()

    def get_port(self):
        net_list = psutil.net_connections()
        ret_list = []
        string = ""
        for net in net_list:
            pid = net.pid
            if psutil.pid_exists(pid):
                process = psutil.Process(pid)
                laddr = net.laddr
                dict = {"ip": laddr.ip, "port": laddr.port, "id": process.pid, "name": process.name(),
                        "status": process.status()}
                ret_list.append(str(dict))
            string = "*".join(ret_list)
        return string

    def kill(self, _pid):
        if (psutil.pid_exists(_pid)):
            process = psutil.Process(_pid)
            print("即将杀死", pid, "进程")
            process.kill()

    def noblocking(self):
        time.sleep(2)
        recv_data = self.SOCKET.recvfrom(self.BUFFER_SIZE)
        return recv_data

def sayHello():
    client = Client()
    client.open()
    client.send("hello", "192.168.43.220", 12349)
    client.close()

def get(addr):
    client = Client()
    client.open()
    client.send(client.get_port(), addr[0], 12349)
    client.close()

def send(request, ip, port):
    print(request, ip, port)
    client = Client()
    client.open()
    client.send(request, ip, port)
    client.close()
#首先给服务端发一个消息，让他知道已经连上

port_list = [12378, 12346, 12349]

net_list = psutil.net_connections()
for net in net_list:
    if net.laddr.port in net_list:
        pid = net.pid
        if psutil.pid_exists(pid):
            process = psutil.Process(12378)
            print("即将杀死", 12378, "进程")
            process.kill()

print("ok!")

data = "sdfs"
ip = None
while True:
    sayHello()
    client = Client()
    client.open()
    client.bind(12378)
    client.SOCKET.settimeout(3)
    try:
        data = client.recv()
        ip = data[1]
        data = data[0].decode('utf-8')
    except BaseException:
        print("！！")
    # print(data)
    if(data == "hello"):
        break
print("已连接到", ip)
client.close()

#此时已经让服务端知道你的ip了
#发送之后就一直等待服务器给你的消息就好了

client = Client()
client.open()
client.bind(12346)

while True:
    data = client.recv()
    if data[0].decode('utf-8') == "get":
        try:
            get(data[1])
        except:
            print("查询错误！")

    if data[0].decode('utf-8') == "kill":
        pid = client.recv()[0].decode('utf-8')
        try:
            client.kill(int(pid))
        except BaseException as e:
            print(e)

    if data[0].decode('utf-8') == "quit":
        break

client.close()