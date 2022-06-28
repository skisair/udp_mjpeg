import requests
import cv2
import numpy as np

if __name__ == '__main__':
    """
    b'--frame\r\n'
    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'
    """
    split = '--frame\r\nContent-Type: image/jpeg\r\n\r\n'.encode()
    r = requests.get('http://localhost:5000', stream=True)
    buffer = b''
    for chunk in r.iter_content(chunk_size=1024):
        if chunk:
            buffer += chunk
        else:
            continue

        while True:
            index = buffer.find(split)
            if index >= 0:
                image = buffer[:index]
                buffer = buffer[index + len(split):]
                if len(image) == 0:
                    continue
                image = image[:-4]
                img_buf= np.frombuffer(image, dtype=np.uint8)
                print(f'img_buf:{img_buf}')
                img = cv2.imdecode(img_buf, cv2.IMREAD_UNCHANGED)
                cv2.imshow('img', img)
                cv2.waitKey(1)
            else:
                break
