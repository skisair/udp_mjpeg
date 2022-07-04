import cv2


class VideoCamera(object):
    def __init__(self, debug: bool = False):
        self.video = cv2.VideoCapture(0)
        self.debug = debug

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        if self.debug:
            cv2.imshow('img', image)
            cv2.waitKey(1)
        return jpeg.tobytes()
