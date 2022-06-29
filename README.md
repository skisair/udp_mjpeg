# udp_mjpeg

UDPによるMJPEG配信・受信テストプログラム

## 環境構築
### Pythonのインストールと環境構築

Python.jpを参考に、pythonとpipをインストール。

https://www.python.jp/install/windows/install.html

仮想環境の設定(Windows PowerShellを起動)
```
.\venv\Scripts\activate.ps1
```

ライブラリ群のインストール
```
pip install -r requirements.txt
```

## TCP版

### サーバの起動

PowerShellからvenvに入り、以下のコマンドを実行する。
```
python tcp_server.py
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
python tcp_client.py
```

TCP版のクライアントは、HTTP GETで動画の取得を行う。
ストリーム上に存在するJPEGイメージをJPEGフォーマットのヘッダ・フッタを元に取得し、表示を行う。

コンソールへは、転送レート、フレームレート、画像圧縮レートを表示する。
