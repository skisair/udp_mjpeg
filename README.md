# MotionJPEG 表示ツール

UDPによるMJPEG配信・受信テストプログラム

## 環境構築
### Pythonのインストールと環境構築

Python.jpを参考に、pythonとpipをインストール。

https://www.python.jp/install/windows/install.html

仮想環境の設定(Windows PowerShellを起動)
```
PS> .\venv\Scripts\activate.ps1
```

ライブラリ群のインストール(コンソールに"(venv)"と表記されていることを確認)
```
(venv) PS> pip install -r requirements.txt
```

## Streamlit版クライアント

PowerShellからvenvに入り、以下のコマンドを実行する。
```
(venv) PS> streamlit run ./streamlit_client.py
```

左側パネルの、Protocol、Host、Portからそれぞれ設定を行うことが可能。

画像下の構造体は、転送レート：bps(M bit / sec)、フレームレート:fps（Frame / sec）、圧縮率:rate （転送JPEGサイズ / ビットマップサイズ）

show graphのチェックを入れることで、１秒ごとにグラフを描画する。


## UDP版（テスト用）

### サーバの起動

PowerShellからvenvに入り、以下のコマンドを実行する。
```
(venv) PS> python .\udp_server.py -h
```
デフォルトで、ポート番号 8000でブロードキャストを行うが、
以下のように引数を指定することでポートの変更、宛先ホストの指定が可能。
カメラの画像を表示する際には、-sを指定することで、ウィンドウ表示を行う。
```
(venv) PS> python .\udp_server.py -h
usage: udp_server.py [-h] [-s] [-p PORT] [-t HOST] [-c CHUNK_SIZE]

optional arguments:
  -h, --help            show this help message and exit
  -s, --show_image      show pictures in cv2 window.
  -p PORT, --port PORT  publish udp port.(system env UDP_PORT)
  -t HOST, --host HOST  publish target host.(system env UDP_TARGET)
  -c CHUNK_SIZE, --chunk_size CHUNK_SIZE
                        datagram size.(system env CHUNK_SIZE)
```

コンソールへは、転送レート、フレームレート、画像圧縮レートを表示する。
```
bps:21.72 Mbps / fps:27.92 fps / rate:11.06 %
bps:21.74 Mbps / fps:27.95 fps / rate:11.06 %
bps:21.67 Mbps / fps:27.86 fps / rate:11.06 %
```

また、以下の通り環境変数を設定することで、引数未指定で起動することも可能。
```
(venv) PS> $ENV:UDP_TARGET="<broadcast>"
(venv) PS> $ENV:UDP_PORT=8000
```


### クライアントの起動


PowerShellからvenvに入り、以下のコマンドを実行する。
```
(venv) PS> python udb_client.py
```

UDP版のクライアントは、ポート8000で待ち受けを行い動画の取得を行う。
ストリーム上に存在するJPEGイメージをJPEGフォーマットのヘッダ・フッタを元に取得し、表示を行う。

コンソールへは、転送レート、フレームレート、画像圧縮レートを表示する。
```
bps:21.91 Mbps / fps:28.16 fps / rate:11.07 %
bps:23.26 Mbps / fps:29.91 fps / rate:11.06 %
bps:23.28 Mbps / fps:29.92 fps / rate:11.06 %
```

待ち受けポートを変更する際には、起動前に以下のように環境変数に設定
```
(venv) PS> $ENV:UDP_PORT=8000
```

## TCP版(おまけ)

### サーバの起動

PowerShellからvenvに入り、以下のコマンドを実行する。
```
(venv) PS> python tcp_server.py
```

TCP版のサーバーは、multipart/x-mixed-replaceで配信する。以下の形式で動画を配信する。
```
--frame\r\n
Content-Type: image/jpeg\r\n
\r\n
"JPEGイメージ"
\r\n
\r\n
```
http://localhost:5000

にブラウザでアクセスすると、PCにWebカメラが搭載されている場合には、 動画が表示される。

### クライアントの起動

PowerShellからvenvに入り、以下のコマンドを実行する。
```
(venv) PS> python tcp_client.py
```

TCP版のクライアントは、HTTP GETで動画の取得を行う。
ストリーム上に存在するJPEGイメージをJPEGフォーマットのヘッダ・フッタを元に取得し、表示を行う。

コンソールへは、転送レート、フレームレート、画像圧縮レートを表示する。
