import os
import socket

from camera import VideoCamera

HOST_NAME = os.environ.get('UDP_TARGET', default='')
PORT = int(os.environ.get('UDP_PORT', default='8000'))

UDP_MAX_SIZE = 65507

if __name__ == '__main__':

    # ipv4を使うので、AF_INET
    # udp通信を使いたいので、SOCK_DGRAM
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # ブロードキャストを行うので、設定
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    camera = VideoCamera()
    while True:
        frame = camera.get_frame()
        while len(frame) > 0:
            datagram = frame[:UDP_MAX_SIZE]
            frame = frame[UDP_MAX_SIZE:]
            # データ送信
            sock.sendto(datagram, ("<broadcast>", PORT))

    sock.close()
