import socket
import time
import psutil


class Server:
    SOCKET = None
    BUFFER_SIZE = 102400
    PORT = 12350

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


def sayHello(ip):
    client = Server()
    client.open()
    client.send("hello", ip, 12378)
    client.close()


def con():
    s = Server()
    s.open()
    ip_list = []
    s.SOCKET.settimeout(5)
    s.SOCKET.bind(("", 12349))
    while True:
        try:
            data = s.recv()
            ip_list.append(data[1][0])
            print(data[1][0])
            sayHello(data[1][0])
        except BaseException:
            break
    print(ip_list)
    s.close()
    return ip_list


def load_get():
    s = Server()
    s.open()
    s.bind(12349)
    data = s.recv()[0].decode("utf-8")
    item_list = data.split('*')
    data = []
    for item in item_list:
        data.append(eval(item))
    s.close()
    return data


def get_resp():
    s = Server()
    s.open()
    s.bind(12350)
    print("wait!")
    data = s.recv()[0].decode("utf-8")
    s.close()
    return data


def say(ip, request, pid):
    s = Server()
    s.open()

    s.send(request, ip, 12346)

    if request == "get":
        return load_get()

    if request == "kill":
        print("kill", ip, pid)
        s.send(pid, ip, 12346)
        return True

    s.close()


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
flag = True

# while True:
#     con()
#     while True:
#         try:
#             req = say()
#             if(req == "quit"):
#                 break
#         except BaseException:
#             print("请重新输入")
