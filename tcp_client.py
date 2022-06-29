import requests

from jpeg_stream_viewer import JpegStreamViewer


if __name__ == '__main__':
    r = requests.get('http://localhost:5000', stream=True)
    jpeg_stream_viewer = JpegStreamViewer()
    for chunk in r.iter_content(chunk_size=1024):
        jpeg_stream_viewer.send(chunk)
