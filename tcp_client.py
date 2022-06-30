import requests

import cv2

from jpeg_stream_viewer import JpegStreamProcessor


if __name__ == '__main__':
    r = requests.get('http://localhost:5000', stream=True)
    jpeg_stream_viewer = JpegStreamProcessor()
    for chunk in r.iter_content(chunk_size=1024):
        for image, stats in jpeg_stream_viewer.send(chunk):
            cv2.imshow('img', image)
            cv2.waitKey(1)
