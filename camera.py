import os
import time

import cv2
import numpy as np


class VideoCamera(object):

    # 移動平均配列要素数
    AVERAGE_SPAN = int(os.environ.get('AVERAGE_SPAN', default='100'))

    def __init__(self, show_image: bool = False):
        """
        デバッグオンで画像表示
        :param show_image:
        """
        self.video = cv2.VideoCapture(0)
        self.show_image = show_image

        # 統計情報表示用
        # 最終画像送信時刻
        self.last_frame_time = time.perf_counter()
        # チャンクサイズ
        self.chunks = []
        # フレーム送信時間
        self.frame_times = []
        # 圧縮率
        self.compression_rate = []

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        if success & self.show_image:
            cv2.imshow('img', image)
            cv2.waitKey(1)
        if success:
            ret, jpeg = cv2.imencode('.jpg', image)
            self._add_stats(image, jpeg)
            self.show_stats()
            return jpeg.tobytes()
        else:
            return None

    def show_stats(self):
        """
        統計情報の表示
        :return:
        """
        print(f'bps:{self.get_bps():.2f} Mbps / '
              f'fps:{self.get_fps():.2f} fps / '
              f'rate:{self.get_compression_rate():.2f} %')

    def _add_stats(self, image, jpeg):
        """
        フレームレートの計算
        :param current_time:
        :return:
        """
        if image is None:
            return
        size = 1
        for i in image.shape:
            size *= i
        rate = len(jpeg) * 100 / size
        current_time = time.perf_counter()
        self.frame_times.append(current_time - self.last_frame_time)
        self.chunks.append(len(jpeg))
        self.compression_rate.append(rate)
        if len(self.frame_times) > VideoCamera.AVERAGE_SPAN:
            self.frame_times = self.frame_times[1:]
            self.chunks = self.chunks[1:]
            self.compression_rate = self.compression_rate[1:]
        self.last_frame_time = current_time

    def get_compression_rate(self):
        """
        圧縮率の取得
        :return:
        """
        rate = np.average(self.compression_rate)
        return rate

    def get_bps(self):
        """
        転送レートの取得（Mbps）
        :return:
        """
        bps = (sum(self.chunks) / sum(self.frame_times)) * 8 / (1024 * 1024)
        return bps

    def get_fps(self):
        """
        フレームレートの取得
        :return:
        """
        fps = len(self.frame_times) / sum(self.frame_times)
        return fps
