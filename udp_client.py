import os
import socket

from jpeg_stream_viewer import JpegStreamViewer

HOST_NAME = os.environ.get('UDP_TARGET', default='')
PORT = int(os.environ.get('UDP_PORT', default='8000'))

if __name__ == '__main__':

    # ipv4を使うので、AF_INET
    # udp通信を使いたいので、SOCK_DGRAM
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # ブロードキャストするときは255.255.255.255と指定せずに空文字
    sock.bind((HOST_NAME, PORT))
    jpeg_stream_viewer = JpegStreamViewer()
    while True:
        # データを待ち受け
        rcv_data, addr = sock.recvfrom(65507)
        jpeg_stream_viewer.send(rcv_data)

    sock.close()
