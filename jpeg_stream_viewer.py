import os
import time

import cv2
import numpy as np


class JpegStreamProcessor:
    
    # 移動平均配列要素数
    AVERAGE_SPAN = int(os.environ.get('AVERAGE_SPAN', default='100'))

    # JPEGフォーマット
    # https://www.setsuki.com/hsp/ext/jpg.htm
    SOI = bytes.fromhex('0xFFD8'[2:])
    EOI = bytes.fromhex('0xFFD9'[2:])

    def __init__(self):
        # バッファ
        self.buffer = b''

        # 統計情報表示用
        # 最終チャンク受信時刻
        self.last_chunk_time = time.perf_counter()
        # 最終画像受信時刻
        self.last_frame_time = time.perf_counter()
        # チャンク受信時間
        self.chunk_times = []
        # チャンクサイズ
        self.chunks = []
        # フレーム受信時間
        self.frame_times = []
        # 圧縮率
        self.compression_rate = []

    def send(self, chunk:bytes):
        """
        チャンクの受信
        :param chunk:
        :return:
        """
        if chunk is None:
            return

        current_time = time.perf_counter()
        self._add_bps_stats(chunk, current_time)
        self.buffer += chunk

        while True:
            # JPEGの先頭と終了を探索
            start_index = self.buffer.find(JpegStreamProcessor.SOI)
            end_index = self.buffer.find(JpegStreamProcessor.EOI)
            if end_index < 0:
                break
            image_buffer = self.buffer[start_index:end_index + len(JpegStreamProcessor.EOI)]
            if image_buffer[2:].find(JpegStreamProcessor.SOI) > 0:
                print(f'SOI:{image_buffer[2:].find(JpegStreamProcessor.SOI) + 2}', start_index, end_index)

            self.buffer = self.buffer[end_index + len(JpegStreamProcessor.EOI):]
            if len(image_buffer) == 0:
                continue

            # イメージの復号
            with open(f'log/{time.perf_counter()}.jpeg', mode='wb') as f:
                f.write(image_buffer)

            image = self.decode_image(image_buffer)
            self._add_fps_stats(current_time)
            stats = {
                'bps': self.get_bps(),
                'fps': self.get_fps(),
                'rate': self.get_compression_rate(),
            }
            yield image, stats
            self.show_stats()

    def decode_image(self, image_buffer):
        """
        イメージバッファを画像イメージにデコード
        :param image_buffer:
        :return:
        """
        img_buf = np.frombuffer(image_buffer, dtype=np.uint8)
        img = cv2.imdecode(img_buf, cv2.IMREAD_UNCHANGED)
        self._add_compression_rate(img, img_buf)
        return img

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
        bps = (sum(self.chunks) / sum(self.chunk_times)) * 8 / (1024 * 1024)
        return bps

    def get_fps(self):
        """
        フレームレートの取得
        :return:
        """
        fps = len(self.frame_times) / sum(self.frame_times)
        return fps

    def show_stats(self):
        """
        統計情報の表示
        :return:
        """
        print(f'bps:{self.get_bps():.2f} Mbps / '
              f'fps:{self.get_fps():.2f} fps / '
              f'rate:{self.get_compression_rate():.2f} %')

    def _add_fps_stats(self, current_time):
        """
        フレームレートの計算
        :param current_time:
        :return:
        """
        self.frame_times.append(current_time - self.last_frame_time)
        if len(self.frame_times) > JpegStreamProcessor.AVERAGE_SPAN:
            self.frame_times = self.frame_times[1:]
        self.last_frame_time = current_time

    def _add_bps_stats(self, chunk, current_time):
        """
        転送レートの計算
        :param chunk:
        :param current_time:
        :return:
        """
        self.chunk_times.append(current_time - self.last_chunk_time)
        self.chunks.append(len(chunk))
        if len(self.chunk_times) > JpegStreamProcessor.AVERAGE_SPAN:
            self.chunk_times = self.chunk_times[1:]
            self.chunks = self.chunks[1:]
        self.last_chunk_time = current_time

    def _add_compression_rate(self, img, img_buf):
        """
        圧縮率の計算
        :param img: 圧縮前（1次元）
        :param img_buf: 圧縮後（２次元＋色）
        :return:
        """
        size = 1
        if img is None:
            return

        for i in img.shape:
            size *= i
        rate = len(img_buf) * 100 / size
        self.compression_rate.append(rate)
        if len(self.compression_rate) > JpegStreamProcessor.AVERAGE_SPAN:
            self.compression_rate = self.compression_rate[1:]
