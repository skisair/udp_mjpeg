import os
import socket

HOST_NAME = os.environ.get('UDP_TARGET', default='')
PORT = int(os.environ.get('UDP_PORT', default='8080'))


if __name__ == '__main__':
    # ipv4を使うので、AF_INET
    # udp通信を使いたいので、SOCK_DGRAM
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # ブロードキャストするときは255.255.255.255と指定せずに空文字
    sock.bind((HOST_NAME, PORT))
    while True:
        # データを待ち受け
        rcv_data, addr = sock.recvfrom(1024)
        print("receive data : [{}]  from {}".format(rcv_data,addr))

    sock.close()