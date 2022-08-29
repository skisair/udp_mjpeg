import os
import socket
import time
from datetime import datetime
import requests

import streamlit as st
import cv2
from PIL import Image
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
from plotly.subplots import make_subplots

from jpeg_stream_viewer import JpegStreamProcessor

UDP_TARGET = os.environ.get('UDP_TARGET', default='')
TCP_TARGET = os.environ.get('TCP_TARGET', default='localhost')
UDP_PORT = int(os.environ.get('UDP_PORT', default='65000'))
TCP_PORT = int(os.environ.get('TCP_PORT', default='8000'))
DATAGRAM_SIZE = int(os.environ.get('DATAGRAM_SIZE', default='65507'))

df = pd.DataFrame(columns=['time', 'bps', 'fps', 'rate',])


def disp(protocol: str, host: str, port: int, show_graph):
    global df
    # ipv4を使うので、AF_INET
    # udp通信を使いたいので、SOCK_DGRAM
    try:
        if protocol == 'UDP':
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # ブロードキャストするときは255.255.255.255と指定せずに空文字
            sock.bind((host, port))
            st.header("UDP Stream Viewer")
        else:
            response = requests.get(f'http://{host}:{port}', stream=True)
            tcp_iter = response.iter_content(chunk_size=1024)
            st.header("TCP Stream Viewer")

        jpeg_stream_viewer = JpegStreamProcessor()


        image_loc = st.empty()
        stats_loc = st.empty()
        graph = st.empty()
        last_update = time.perf_counter()
        while True:
            # データを待ち受け
            if protocol == 'UDP':
                rcv_data, address = sock.recvfrom(DATAGRAM_SIZE)
            else:
                rcv_data = next(tcp_iter)

            for image, stats in jpeg_stream_viewer.send(rcv_data):
                image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                image_loc.image(image, width=640)
                stats_loc.write(stats)
                if not show_graph:
                    continue

                if time.perf_counter() - last_update > 1.0:
                    stats['time'] = datetime.now()
                    df_append = pd.DataFrame(data=[stats.values()], columns=stats.keys())
                    df = pd.concat([df, df_append])
                    with graph:
                        subfig = make_subplots(specs=[[{"secondary_y": True}]])
                        fig1 = px.line(df[-30:], x="time", y=["fps"],)
                        fig2 = px.line(df[-30:], x="time", y=["bps"],)
                        fig2.update_traces(yaxis='y2')
                        subfig.add_traces(fig1.data + fig2.data)
                        subfig.layout.xaxis.title="Time"
                        subfig.layout.yaxis.title="fps"
                        subfig.layout.yaxis2.title="Mbps"
                        subfig.layout.yaxis.range = [0, 60]
                        subfig.layout.yaxis2.range = [0, 60]
                        subfig.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))
                        graph.write(subfig)
                    last_update = time.perf_counter()
    except Exception as e:
        st.write(e)
        if protocol == 'UDP':
            sock.close()


def main():
    st.sidebar.title('接続先の設定')
    protocol = st.sidebar.selectbox('protocol', ('UDP', 'TCP'))
    if protocol == 'UDP':
        host = st.sidebar.text_input('host:', value=UDP_TARGET)
        port = st.sidebar.number_input('port：', value=UDP_PORT)
    else:
        host = st.sidebar.text_input('host:', value=TCP_TARGET)
        port = st.sidebar.number_input('port：', value=TCP_PORT)

    show_graph = st.sidebar.checkbox('show graph', value=False)
    disp(protocol, host, port, show_graph)


if __name__ == '__main__':
    main()