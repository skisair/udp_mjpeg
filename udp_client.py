import os
import socket
import time
import cv2

from jpeg_stream_viewer import JpegStreamProcessor

HOST_NAME = os.environ.get('UDP_TARGET', default='')
PORT = int(os.environ.get('UDP_PORT', default='58000'))
# DATAGRAM_SIZE = int(os.environ.get('DATAGRAM_SIZE', default='1024'))
DATAGRAM_SIZE = int(os.environ.get('DATAGRAM_SIZE', default='65507'))


def main():
    # ipv4を使うので、AF_INET
    # udp通信を使いたいので、SOCK_DGRAM
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', PORT))
    print(sock)
    jpeg_stream_viewer = JpegStreamProcessor()
    while True:
        # データを待ち受け
        rcv_data, addr = sock.recvfrom(DATAGRAM_SIZE)
        with open(f'log/stream.bin', mode='ab') as f:
            f.write(rcv_data)
        # print(f"message: {rcv_data}\nfrom: {addr}")
        for image, stats in jpeg_stream_viewer.send(rcv_data):
            cv2.imshow('img', image)
            cv2.waitKey(1)

    sock.close()


if __name__ == '__main__':
    main()
