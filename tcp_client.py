import time

import requests
import cv2
import numpy as np

SOI = bytes.fromhex('0xFFD8'[2:])
EOI = bytes.fromhex('0xFFD9'[2:])

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
        current_time = time.perf_counter()
        if chunk:
            buffer += chunk
            chunk_times.append(current_time - last_chunk_time)
            chunks.append(len(chunk))
            last_chunk_time = current_time
            if len(chunk_times) > 100:
                chunk_times = chunk_times[1:]
                chunks = chunks[1:]
        else:
            continue

        while True:
            start_index = buffer.find(SOI)
            end_index = buffer.find(EOI)
            if end_index >= 0:
                image = buffer[start_index:end_index]
                buffer = buffer[end_index + len(EOI):]
                if len(image) == 0:
                    continue

                frame_times.append(current_time - last_frame_time)
                last_frame_time = current_time
                img_buf= np.frombuffer(image, dtype=np.uint8)
                img = cv2.imdecode(img_buf, cv2.IMREAD_UNCHANGED)
                cv2.imshow('img', img)
                cv2.waitKey(1)
                if len(frame_times) > 100:
                    frame_times = frame_times[1:]
                    frames = frames[1:]
                print(f'bps:{(sum(chunks) / sum(chunk_times)) * 8 / (1024 * 1024):.2f} Mbps / '
                      f'fps:{len(frame_times) / sum(frame_times):.2f} fps')
            else:
                break
