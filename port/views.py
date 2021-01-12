from django.shortcuts import render
from . import port
from . import server


# Create your views here.

def index(request):
    item_list = port.self_port_get().split('*')
    port_list = []
    for item in item_list:
        port_list.append(eval(item))
    context = {
        "port_list": port_list
    }
    return render(request, 'index/index.html', context)


def index_del(request, pid):
    port.del_self_port(pid)
    item_list = port.self_port_get().split('*')
    port_list = []
    for item in item_list:
        port_list.append(eval(item))
    context = {
        "port_list": port_list
    }
    return render(request, 'index/index.html', context)


def local_ip(request):
    ip_list = port.get_all_ip()
    context = {
        "ip_list": ip_list
    }
    return render(request, 'index/local_ip.html', context)


def local_ip_port(request, ip):
    port_list = port.get_port_status(ip)
    context = {
        "port_list": port_list
    }
    return render(request, 'index/local_ip_port.html', context)


def search_any_port(request):
    return render(request, 'index/search_any_port.html')


def search(request):
    ip = request.POST['ip']
    search_port = int(request.POST['search_port'])

    if search_port == 0:
        port_list = port.get_port_status(ip)
    else:
        port_list = [port.search_port_status(ip, search_port)]

    context = {
        "port_list": port_list
    }
    return render(request, 'index/search.html', context)


def listen(request):
    ip_list = server.con()
    context = {
        "ip_list": ip_list
    }
    return render(request, 'index/listen.html', context)


def listen_port(request, ip):
    port_list = server.say(ip, "get", 0)
    context = {
        'ip': ip,
        "port_list": port_list
    }
    return render(request, 'index/listen_port.html', context)


def kill_port(request, ip, pid):
    server.say(ip, "kill", str(pid))
    port_list = server.say(ip, "get", 0)
    context = {
        'ip': ip,
        "port_list": port_list
    }
    return render(request, 'index/listen_port.html', context)


def quit_con(request, ip):
    server.say(ip, "quit", 0)
    ip_list = server.con()
    context = {
        "ip_list": ip_list
    }
    return render(request, 'index/listen.html', context)