import argparse

import os
import socket

from camera import VideoCamera

HOST_NAME = os.environ.get('UDP_TARGET', default='<broadcast>')
PORT = int(os.environ.get('UDP_PORT', default='8000'))

UDP_MAX_SIZE = int(os.environ.get('CHUNK_SIZE', default='65507'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--show_image', help='show pictures in cv2 window.', action='store_true')
    parser.add_argument('-p', '--port', type=int, default=PORT, help='publish udp port.(system env UDP_PORT)')
    parser.add_argument('-t', '--host', type=str, default=HOST_NAME, help='publish target host.(system env UDP_TARGET)')
    parser.add_argument('-c', '--chunk_size', type=int, default=UDP_MAX_SIZE,
                        help='datagram size.(system env CHUNK_SIZE)')

    args = parser.parse_args()
    # ipv4を使うので、AF_INET
    # udp通信を使いたいので、SOCK_DGRAM
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # ブロードキャストを行うので、設定
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    camera = VideoCamera(show_image=args.show_image)
    while True:
        frame = camera.get_frame()
        while len(frame) > 0:
            datagram = frame[:args.chunk_size]
            frame = frame[args.chunk_size:]
            # データ送信
            sock.sendto(datagram, (args.host, args.port))

    sock.close()
