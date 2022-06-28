import time

import requests
import cv2
import numpy as np

from jpeg_stream_viewer import JpegStreamViewer

SOI = bytes.fromhex('0xFFD8'[2:])
EOI = bytes.fromhex('0xFFD9'[2:])

jpeg_stream_viewer = JpegStreamViewer()

if __name__ == '__main__':
    r = requests.get('http://localhost:5000', stream=True)
    buffer = b''
    last_chunk_time = time.perf_counter()
    last_frame_time = time.perf_counter()
    chunk_times = []
    frame_times = []
    chunks = []
    frames = []
    for chunk in r.iter_content(chunk_size=1024):
        jpeg_stream_viewer.send(chunk)
