from flask import Flask, Response

from camera import VideoCamera


app = Flask(__name__)


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n'
               b'\r\n' +
               frame +
               b'\r\n'
               b'\r\n')


@app.route('/')
def video_feed():
    return Response(
        gen(VideoCamera()),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
