import socket, time

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    if sock.connect_ex(('192.168.0.151', 23)) == 0:
        _ = sock.recv(1024)
        sock.send(b'root\r\n')
        time.sleep(0.1)
        _ = sock.recv(1024)
        sock.send(b'root2root\r\n')
        time.sleep(0.1)
        _ = sock.recv(1024)
        sock.send(b'reboot\r\n')
        time.sleep(0.1)
        _ = sock.recv(1024)

